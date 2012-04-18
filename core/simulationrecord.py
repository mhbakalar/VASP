import re
import scipy as sp
from vaspsimulation import VaspSimulation

class SimulationRecord:

    def __init__(self, filepath, vasp_simulation=None, mode='w'):
        self.file = None
        self.mode = mode
        if mode == 'w':
            self.vasp_simulation = vasp_simulation
            self.filepath = filepath
        elif mode == 'r':
            self.filepath = filepath
    
    def __getitem__(self, val):
        line = self.next_state()
        if line == None:
            raise IndexError("End of file")
        else:
            return line

    def __len__(self):
        if self.file == None:
            self.open_file()
        self.file.seek(0)
        i = 0
        for line in self.file:
            i += 1
        self.file.seek(0)
        return i

    def max_lattice_size(self):
        max_size = 0
        for item in self:
            content_size = len(item[1])
            if content_size > max_size:
                max_size = content_size
        return max_size
        
    def open_file(self):
        self.file = open(self.filepath, self.mode)

    def close_file(self):
        self.file.close()
        self.file = None

    def save_state(self):
        lattice = self.vasp_simulation.lattice
        time = self.vasp_simulation.time
        curr_lattice = lattice.current_lattice()
        value = str(time) + ': ' + self.arr_to_str(curr_lattice) + '\n'
        self.file.write(value)

    def arr_to_str(self, arr):
        strrep = '['
        for element in arr:
            strrep += str(element)
            strrep += ', '
        strrep += 'end]'
        return strrep

    def recover_state(self, state_str):
        exp = '([0-9]+\.[0-9]+[e]?[\-0-9]*): \[(([0-9]+\.[0-9]*, )+)end\]'
        try:
            matches = re.match(exp, state_str)
            time_str = matches.group(1)
            time = float(time_str)
            lattice_str = matches.group(2).split()
            lattice_contents = sp.array([int(float(e.strip(','))) for e in lattice_str])
            return (time, lattice_contents)
        except:
            print state_str

    def next_state(self):
        if self.file == None:
          self.open_file()
        line = self.file.readline()
        if line == '':
            return None
        else:
            return self.recover_state(line)
