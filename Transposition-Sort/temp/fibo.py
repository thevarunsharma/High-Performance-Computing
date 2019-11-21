import threading
import queue

Q = queue.Queue()

def fib(n):
    if n <= 1:
        return n
    proc = threading.Thread(target=lambda q, arg1: Q.put(fib(arg1)), args=(Q, n-1,))
    proc.start()
    y = fib(n-2)
    proc.join()
    x = Q.get()
    return x + y

n = int(input("Enter N:"))
for i in range(1, n+1): print(fib(i))
