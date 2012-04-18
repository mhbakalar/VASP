import random
import scipy as sp
from latticemodel import LatticeModel

class VaspSimulation:

    VASP_ON_BASE = 1.0
    VASP_ON = VASP_ON_BASE
    VASP_OFF = .008
    VASP_DIFFUSE = 1.0
    POLYMERIZE = 4.0

    '''
    Transition Events
    ''' 

    def rate_on_event(self):
        rate = VaspSimulation.VASP_ON * self.lattice.number_open
        return rate

    def on_event(self):
        self.lattice.insert_particle(self.lattice.random_open())
        
    def rate_off_event(self):
        rate = VaspSimulation.VASP_OFF * self.lattice.number_occupied
        return rate

    def off_event(self):
        self.lattice.remove_particle(self.lattice.random_occupied())

    def rate_diffuse_event(self):
        rate = VaspSimulation.VASP_DIFFUSE * self.lattice.number_occupied
        return rate

    def diffuse_event(self):
        position = self.lattice.random_occupied()
        direction = random.randint(0, 1)
        if direction == 0:
            if self.lattice[position - 1] == 0:
                self.lattice[position] = 0
                self.lattice[position - 1] += 1
        else:
            if self.lattice[position + 1] == 0:
                self.lattice[position] = 0
                self.lattice[position + 1] += 1

    def rate_polymerize_event(self):
        if self.lattice.head_occupied > 0:
            rate = VaspSimulation.POLYMERIZE
        else:
            rate = 0
        return rate

    def polymerize_event(self):
        self.lattice.grow()
        self.lattice[self.lattice.lattice_ptr-1] += 1
        self.lattice[self.lattice.lattice_ptr-2] -= 1

    def polymerize_non_processive_event(self):
        self.lattice.grow()

    def polymerize_detach_event(self):
        self.lattice.grow()
        self.lattice[self.lattice.lattice_ptr-2] -= 1

    '''
    End Transition Events
    '''

    def __init__(self, lattice, mode='processive'):
        self.time = 0
        self.lattice = lattice

        self.define_transitions()
        if mode == 'nonprocessive':
            self.events['polymerize'] = (self.rate_polymerize_event,
                                         self.polymerize_non_processive_event)
        elif mode == 'detach':
            self.events['polymerize'] = (self.rate_polymerize_event,
                                         self.polymerize_detach_event)  

    def define_transitions(self):
        self.events = {"vasp_on": (self.rate_on_event, self.on_event),
              "vasp_off": (self.rate_off_event, self.off_event),
              "vasp_diffuse": (self.rate_diffuse_event, self.diffuse_event),
              "polymerize": (self.rate_polymerize_event, self.polymerize_event)}

    def compute_cumulative_rate(self):
        cumrate = 0.0
        for key in self.events:
            rate_function = self.events[key][0]
            rate = rate_function()
            cumrate += rate
        return cumrate
        
    def choose_event(self):
        randnum = random.uniform(0, 1)
        cumrate = self.compute_cumulative_rate()
        if cumrate == 0:
            raise Exception("No events available. Simulation hit a dead end")
        else:
            ratehit = randnum * cumrate
            n = 0
            for key in self.events:
                rate_function = self.events[key][0]
                rate = rate_function()
                n += rate
                if n > ratehit:
                    break
            randnum = random.uniform(0, 1)
            time_step = -(sp.log(randnum)/cumrate)
            return (key, time_step)

    def advance_simulation(self):
        (event, time_step) = self.choose_event()
        self.time += time_step
        eventfunc = self.events[event][1]
        eventfunc()
    

