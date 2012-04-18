from core.latticemodel import LatticeModel
from core.vaspsimulation import VaspSimulation
from core.simulationrecord import SimulationRecord
from core.timereconstruction import TimeReconstruction
from matplotlib import pyplot
from scipy import polyfit, polyval
import scipy as sp

class ConcScan:
    
    @staticmethod
    def Simulate():
        
        record_path = '/Users/matthewbakalar/projects/VASP/latticerecord2.dat'
        simulation_steps = 100
        initial_size = 10
        max_size = 10000

        c_steps = 10
        c_multiplier = 10
        c_range = sp.zeros(c_steps)
        c_range[0] = .0001
    
        for i in range(1,c_steps):
            c_range[i] = c_range[i-1] * c_multiplier

        error = sp.zeros(c_range.size)
        a = sp.zeros(c_range.size)
        b = sp.zeros(c_range.size)

        count = 0
        for conc in c_range:

            lattice = LatticeModel(initial_size, max_size)
            simulation = VaspSimulation(lattice)
            record = SimulationRecord(record_path, simulation, 'w')

            record.open_file()

            VaspSimulation.VASP_ON = VaspSimulation.VASP_ON_BASE * conc

            for i in range(0, simulation_steps):
                simulation.advance_simulation()
                record.save_state()

            record.close_file()

            record = SimulationRecord(record_path, simulation, 'r')
            time_recon = TimeReconstruction(record)
            lvt = time_recon.length_vs_time()

            #Linear regressison -polyfit - polyfit can be used other orders polys
            n = lvt[0].size
            (ar,br)=polyfit(lvt[0],lvt[1],1)
            xr=polyval([ar,br],lvt[0])
            #compute the mean square error
            err=sp.sqrt(sum((xr-lvt[1])**2)/n)
            print('Linear regression using polyfit')
            print('parameters: regression: a=%.2f b=%.2f, ms error= %.3f' % (ar,br,err))

            pyplot.plot(lvt[0], lvt[1], 'g')
            pyplot.plot(lvt[0], xr, 'r')
            pyplot.show()

            a[count] = ar
            b[count] = br
            error[count] = err

            count+=1
            print 'Count = %(count)d' % {'count':count}
        
