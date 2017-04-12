import sys
import numpy as np

"""
A class for writing and reading data
Features:
- n-dimensional; main dimension is 0
- single write index
- k read indeces
"""

class Ringbuffer(object):

    def __init__(self, dims, parent=None):
        self.windex = 0  # write index
        self.read_indeces = {'default': 0}
        # generate a n-dimensional numpy array
        try:
            self.buffer = np.zeros(dims)
        except:
            print('!! Numpy array could not be generated !!\n')
            sys.exit(sys.exc_info())

    def write(self, data):
        if self.is_overwriting(data.shape[0]):
            raise IOError
        inx = self.windex % self.buffer.shape[0]  # actual index in the buffer
        endx = inx + data.shape[0]  # end index including new data
        if endx <= self.buffer.shape[0]:  # case: new data fits into the buffer 
            # write data into array
            self.buffer[inx:endx] = data
        else:  # case: some data has to be put to the end and some to the start of the array
            endx %= self.buffer.shape[0]
            # write data into array
            self.buffer[inx:, :] = data[:-endx]
            self.buffer[:endx, :] = data[-endx:]  
        # increase write index by data.shape[0]
        self.windex += data.shape[0]

    def read(self, nframes=None, inx_name='default'):
        # return a copy of data for index 'inx_name'
        # if 'inx_name' is not given use default
        # increase index by nframes

        rx = self.read_indeces[inx_name]

        if nframes is None:
            nframes = self.windex - rx
        else:
            nframes = np.min((nframes, self.windex-rx))

        readx = rx % self.buffer.shape[0]
        endx = readx + nframes
        
        if endx <= self.buffer.shape[0]:
            data = np.array(self.buffer[readx:endx])
        else:
            endx %= self.buffer.shape[0]
            data = np.concatenate((self.buffer[readx:], self.buffer[:endx]))
        self.read_indeces[inx_name] += nframes
        return data

    def is_overwriting(self, nframes):
        # check if any data is overwritten without being read
        min_rx = np.min(self.read_indeces.values())
        if self.windex - min_rx + nframes > self.buffer.shape[0]:
            return True
        else:
            return False

    def get_read_index(self, inx_name=None):
        if inx_name is not None:
            return self.read_indeces[inx_name]
        else:
            return self.read_indeces['default']

    def get_data_available(self, inx_name=None):
        rx = self.read_indeces[inx_name]
        return self.windex - rx

    def get_frames(self):
        return self.windex

    def set_new_read_index(self, inx_name, index=0):
        self.read_indeces[inx_name] = index

    def reset_indeces(self):
        """
        resets indeces to the lowest possible value to prevent indeces larger then the biggest possible integer
        """
        shiftx = np.min(self.read_indeces.values())
        self.buffer = np.roll(self.buffer, shiftx, axis=0)
        self.windex -= shiftx
        for key in self.read_indeces.keys():
            self.read_indeces[key] -= shiftx
        return np.min(self.read_indeces.values())  # for control: return the new minimum read index (should be 0)

# #######################################

if __name__ == "__main__":

    # EXAMPLES

    # new buffer
    print('One dimensional ring buffer')
    ring = Ringbuffer((20))

    # writing data
    print('writing ...')
    ring.write(np.random.random((4)))
    print(ring.buffer.T)
    print('\n')
    ring.write(np.random.random((16)))
    print(ring.buffer.T)

    # reading data
    print('\nreading ...')
    print(ring.read(4).T)
    print('\n')
    print(ring.read().T)
    print('\nsecond read index')
    ring.set_new_read_index('no2')
    print(ring.read(4, inx_name='no2').T)
    print('\n')
    print(ring.read(inx_name='no2').T)
    
    # reset indeces
    print('new minimum index after reset: {}'.format(ring.reset_indeces()))

    print('\n\n')

    # new buffer
    print('3 dimensional ring buffer')
    ring = Ringbuffer((6, 2, 2))

    # writing data
    print('writing ...')
    ring.write(np.random.random((1,2,2)))
    print(ring.buffer.T)
    print('\n')
    ring.write(np.random.random((5,2,2)))
    print(ring.buffer.T)

    # reading data
    print('\nreading ...')
    print(ring.read(1).T)
    print('\n')
    print(ring.read().T)
