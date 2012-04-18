import os, datetime
from core.latticemodel import LatticeModel
from core.vaspsimulation import VaspSimulation
from core.simulationrecord import SimulationRecord
from core.timereconstruction import TimeReconstruction
from core import datamanagement
from matplotlib import pyplot
import scipy as sp
from scipy import polyfit


class Experiment:

    LOG = True

    processive = None
    non_processive = None
    detach = None

    record_base = './data'

    initsize = 10
    maxsize = 10000

    equilibrate = 10
    simulate = 100
    conc = 10.**sp.linspace(-2.0, 2.0, 10)

    @staticmethod
    def Setup():
        initsize = Experiment.initsize
        maxsize = Experiment.maxsize
        record_base = Experiment.record_base
        
        lattice = LatticeModel(initsize, maxsize)
        Experiment.processive = VaspSimulation(lattice, mode='processive')

        lattice = LatticeModel(initsize, maxsize)
        Experiment.non_processive = VaspSimulation(lattice, mode='nonprocessive')

        lattice = LatticeModel(initsize, maxsize)
        Experiment.detach = VaspSimulation(lattice, mode='detach')

        Experiment.runs = [(Experiment.processive, 'processive.txt'),
                            (Experiment.non_processive, 'non_processive.txt'),
                            (Experiment.detach, 'detach.txt')]

        Experiment.datafolder = os.path.join(record_base,
                                             datamanagement.datefolder())
        if not os.path.exists(Experiment.datafolder):
            os.makedirs(Experiment.datafolder)
    
    @staticmethod
    def Simulate():        
        for sim, fname in Experiment.runs:
            Experiment.Log('Starting: ' + fname)
            for conc in Experiment.conc:
                Experiment.Log('Concentration: ' + str(conc))
                fname_conc = fname + '_c=' + str(conc)
                pth = os.path.join(Experiment.datafolder, fname_conc)
                
                record = SimulationRecord(pth, sim, 'w')
                record.open_file()
                VaspSimulation.VASP_ON = VaspSimulation.VASP_ON_BASE * conc
                
                while sim.time <= Experiment.equilibrate:
                    sim.advance_simulation()
                    
                sim.time = 0
                while sim.time <= Experiment.simulate:
                    if sim.time % 1 < 0.01:
                        Experiment.Log('Time: ' + str(sim.time))
                    sim.advance_simulation()
                    record.save_state()
                    
                record.close_file()
        
    @staticmethod
    def Save():
        pass
    
    @staticmethod
    def Report():
        imgname = 'polymethodsgrowth.png'
        slopename = 'slopes.txt'
        slopes = sp.zeros([len(Experiment.runs), len(Experiment.conc)])
        i = 0
        j = 0
        pyplot.figure(1)
        for sim, fname in Experiment.runs:
            for conc in Experiment.conc:
                fname_conc = fname + '_c=' + str(conc)
                pth = os.path.join(Experiment.datafolder, fname_conc)
                record = SimulationRecord(pth, sim, 'r')
                recon = TimeReconstruction(record)
                data = recon.constant_interval(len(record))
                pyplot.plot(data[0], data[1])
                (ar,br)=polyfit(data[0],data[1],1)
                slopes[i, j] = ar
                j += 1
            j = 0
            i += 1

        
        # length versus time
        pyplot.legend(('Processive', 'Non-processive', 'Detach'),
                      'upper left', shadow=True, fancybox=False)
        pyplot.xlabel('Time (s)')
        pyplot.ylabel('Filament length')
        pyplot.savefig(os.path.join(Experiment.datafolder, imgname))
        slope_fname = os.path.join(Experiment.datafolder, slopename)
        sp.savetxt(slopename, slopes)

        # slope vs concentration
        pyplot.figure(2)
        pyplot.plot(Experiment.conc, slopes[0])
        pyplot.plot(Experiment.conc, slopes[1])
        pyplot.plot(Experiment.conc, slopes[2])
        pyplot.legend(('Processive', 'Non-processive', 'Detach'),
                      'upper left', shadow=True, fancybox=False)
        pyplot.xscale('log')
        pyplot.xlabel('Concentration')
        pyplot.ylabel('Average Growth Rate')
        
        pyplot.show()
        
    @staticmethod
    def Log(line):
        print line
