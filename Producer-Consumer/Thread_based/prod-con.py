import threading
import random
import time

class Semaphore:
    def __init__(self, init=1):
        self.s = 1

    def wait(self):
        while self.s <= 0:
            pass
        self.s -= 1

    def signal(self):
        self.s += 1

class Buffer:
    def __init__(self, init = 1):
        self.rand_num = init

    def set(self, v):
        self.rand_num = v

    def get(self):
        return self.rand_num

def producer(sema, full, buff, cnt):
    while cnt.get() > 0:
        sema.wait()
        if cnt.get() <= 0:
            return
        print("{0:-^50}".format("PRODUCER"))
        buff.set(random.randrange(-2**31, 2**31-1))
        print("shared variable write: %d"%buff.get())
        full.signal()
        sema.signal()
        time.sleep(0.1)

def consumer(sema, full, buff, cnt):
    while cnt.get() > 0:
        full.wait()
        sema.wait()
        if cnt.get() < 0:
            return
        print("{0:-^50}".format("CONSUMER"))
        print("shared variable read: %d"%buff.get())
        cnt.set(cnt.get()-1)
        sema.signal()
        time.sleep(0.1)

if __name__ == "__main__":
    sema = Semaphore()
    full = Semaphore(0)
    buff = Buffer()
    cnt = Buffer(int(input("How many times?: ")))
    prod = threading.Thread(target=producer, args=(sema, full, buff, cnt))
    cons = threading.Thread(target=consumer, args=(sema, full, buff, cnt))
    prod.start()
    cons.start()
    prod.join()
    cons.join()
    del sema, full, buff, cnt
