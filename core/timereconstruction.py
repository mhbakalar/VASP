import scipy as sp
from simulationrecord import SimulationRecord

class TimeReconstruction:

    def __init__(self, record):
        self.record = record
        
    def length_vs_time(self):
        size = len(self.record)
        time = sp.zeros(size, 'float')
        length = sp.zeros(size, 'int')
        i = 0
        for item in self.record:
            time[i] = item[0]
            length[i] = item[1].size
            i += 1
        return (time, length)

    def raw_data(self):
        size = len(self.record)
        time = sp.zeros(size, 'float')
        max_size = self.recod.max_lattice_size()
        data = sp.zeros([size, max_size], 'int')
        i = 0
        for item in self.record:
            time[i] = item[0]
            lattice_size = item[1].size
            data[i][0:lattice_size-1] = item[1]
            i += 1
        return (time, data)

    def constant_interval(self, time_points):
        lvt = self.length_vs_time()
        max_time = lvt[0][lvt[0].size - 1]
        bins = sp.arange(0, max_time, max_time/time_points)
        time_spots = sp.digitize(lvt[0], bins)
        ts = bins
        ys = sp.zeros(bins.size)
        for i in range(0, lvt[0].size):
            spot = time_spots[i]
            ys[spot-1] = lvt[1][i]

        # Fill in zero values with previous length
        max_val = 0
        for i in range(0, ts.size-1):
            if ys[i] > max_val:
                max_val = ys[i]
            else:
                ys[i] = max_val
        return sp.array([ts, ys])

    def density_vs_time(self):
        size = len(self.record)
        time = sp.zeros(size, 'float')
        density = sp.zeros(size, 'int')
        i = 0
        for item in self.record:
            time[i] = item[0]
            occupancy = sp.average(item[1])
            density[i] = occupancy
            i += 1
        return (time, occupancy)

    def constant_interval_data(self, time_points):
        (time, data) = self.raw_data()
        length = sp.zeros(size, 'int')
        i = 0
        for item in self.record:
            time[i] = item[0]
            length[i] = item[1].size
            i += 1
        return (time, length)
