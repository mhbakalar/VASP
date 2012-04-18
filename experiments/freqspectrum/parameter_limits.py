from latticemodel import LatticeModel
from vaspsimulation import VaspSimulation
from simulationrecord import SimulationRecord
from timereconstruction import TimeReconstruction
from matplotlib import pyplot
from scipy import polyfit, polyval
import scipy as sp
import scipy.fftpack as fftpack
from analysis import *

record_path = '/Users/matthewbakalar/projects/VASP/latticerecord2.dat'
simulation_steps = 100
sim_time = 1000
initial_size = 10
max_size = 10000
concentrations = sp.arange(0.1, 2, 0.1)

verts = fspace_over_runs(record_path, simulation_steps, sim_time,
                         concentrations, initial_size,
                         max_size, 0)
