import random
from multiprocessing import shared_memory
from array import array
from util import wait, signal

mem = shared_memory.SharedMemory(name = 'prod_con_buffer')
buff = mem.buf.cast('i')
print(mem.name)
try:
    while True:
        print("{0:-^50}".format("PRODUCER"))
        seed = int(input("Enter a seed: "))
        wait(buff, 1)
        random.seed = seed
        buff[0] = random.randrange(-2**31, 2**31-1)
        print("shared variable write: %d"%buff[0])
        signal(buff, 2)
        signal(buff, 1)
except KeyboardInterrupt:
    pass
del buff
mem.close()
