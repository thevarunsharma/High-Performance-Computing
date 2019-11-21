from array import array
from multiprocessing import shared_memory
from util import wait, signal

mem = shared_memory.SharedMemory(name = 'prod_con_buffer')
buff = mem.buf.cast('i')
print(mem.name)
try:
    while True:
        wait(buff, 2)
        wait(buff, 1)
        print("{0:-^50}".format("CONSUMER"))
        print("shared variable read: %d"%buff[0])
        signal(buff, 1)
except KeyboardInterrupt:
    pass
del buff
mem.close()
