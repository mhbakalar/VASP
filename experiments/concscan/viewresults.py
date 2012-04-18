import scipy as sp
from matplotlib import pyplot

dpath = "/Users/matthewbakalar/Projects/VASP/c_sweep.dat"
epath = "/Users/matthewbakalar/Projects/VASP/c_sweep_error.dat"

data = sp.genfromtxt(dpath)
error = sp.genfromtxt(epath)

keq = data[0] / (.008)

pyplot.errorbar(keq, data[1])
pyplot.xscale('log')
pyplot.xlabel('Keq (on/off)')
pyplot.ylabel('Rate')
pyplot.title('Polymerization rate vs concentration')
pyplot.show()
