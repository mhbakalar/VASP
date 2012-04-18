import scipy as sp
from scipy import fftpack
from latticemodel import LatticeModel
from vaspsimulation import VaspSimulation
from simulationrecord import SimulationRecord
from timereconstruction import TimeReconstruction
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def fspace_over_runs(record_path, simulation_steps, sim_time, concentrations,
                     initial_size, max_size, equilibrate_steps):

    fspace = sp.zeros([concentrations.size, simulation_steps])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    count = 0
    x = sp.array([])
    y = sp.array([])
    z = sp.array([])
    for conc in concentrations:
        lattice = LatticeModel(initial_size, max_size)
        simulation = VaspSimulation(lattice)
        record = SimulationRecord(record_path, simulation, 'w')

        # Run simulation
        record.open_file()

        VaspSimulation.VASP_ON = VaspSimulation.VASP_ON_BASE * conc

        while simulation.time < sim_time:
            simulation.advance_simulation()
            record.save_state()

        record.close_file()

        # Analyze results
        record = SimulationRecord(record_path, simulation, 'r')
        time_recon = TimeReconstruction(record)
        lvt = time_recon.length_vs_time()
        lvt_const = time_recon.constant_interval(simulation_steps)
        rates = lvt_const[0]
        freqs = fftpack.fftshift(abs(sp.fft(lvt_const[1])))
        my_z = sp.zeros(lvt_const[0].size) + count
        x = sp.append(x, lvt_const[0])
        y = sp.append(y, freqs)
        z = sp.append(z, my_z)
        print count
        count += 1

    ax.set_xlabel('Frequency')
    ax.set_ylabel('Concentration')
    ax.set_zlabel('Power')
    ax.plot_wireframe(x, z, y, rstride=10, cstride=10)
    plt.show()

