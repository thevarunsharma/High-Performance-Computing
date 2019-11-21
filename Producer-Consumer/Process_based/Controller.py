from multiprocessing import shared_memory
from array import array

data = array('i', [1, 1, 0])      # rand_num, semaphore, full
mem = shared_memory.SharedMemory(name = 'prod_con_buffer', create = True, size = data.itemsize * len(data))
buffer = mem.buf.cast('i')
buffer[:] = data[:]
try:
    while True:
        pass
except KeyboardInterrupt:
    pass
del buffer
mem.close()
mem.unlink()
