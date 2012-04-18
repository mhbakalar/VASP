import scipy as sp
import random

class LatticeModel:
    
    def __init__(self, initial_size, max_size):
        self.max_size = max_size
        self.lattice_ptr = initial_size

        # Lattice data model. Store an array of size=max_size. In each position,
        # store number of particles currently occupying that spot. Use -1 to
        # indicate a not yet existent position in the lattice
        positions = sp.array(range(0, self.max_size))
        available = sp.where(positions < initial_size)
        self.lattice = sp.ones(self.max_size) * -1
        self.lattice[available] = 0

    def __getitem__(self, val):
        return self.lattice[val]

    def __setitem__(self, idx, val):
        self.lattice[idx] = val

    def __str__(self):
        current_lattice = self.lattice[sp.where(self.lattice >= 0)]
        return str(current_lattice)

    def current_lattice(self):
        return self.lattice[sp.where(self.lattice >= 0)]

    def grow(self):
        self.lattice[self.lattice_ptr] = 0
        self.lattice_ptr += 1

    @property
    def number_open(self):
        options = sp.where(self.lattice == 0)[0]
        return options.size

    @property
    def number_occupied(self):
        options = sp.where(self.lattice > 0)[0]
        return options.size

    @property
    def head_occupied(self):
        return self.lattice[self.lattice_ptr-1] > 0

    def random_open(self):
        options = sp.where(self.lattice == 0)[0]
        if options.size > 0:
            return options[random.randint(0, options.size-1)]
        else:
            Exception("No open spots")

    def random_occupied(self):
        options = sp.where(self.lattice > 0)[0]
        if options.size > 0:
            return options[random.randint(0, options.size-1)]
        else:
            Exception("No occupied spots")

    def insert_particle(self, position):
        self.lattice[position] += 1

    def remove_particle(self, position):
        self.lattice[position] -= 1
            
