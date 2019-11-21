from cython import nogil, parallel
from cython.parallel import prange

def odd_even_sort(arr):
    n = len(arr)
    for i in range(len(arr)):
        if i & 1 == 0:
            with nogil, parallel.parallel():
                for j in prange(0, n-1, 2):
                    if arr[j] > arr[j+1]:
                        arr[j], arr[j+1] = arr[j+1], arr[j]
        else:
            with nogil, parallel.parallel():
                for j in prange(1, n-1, 2):
                    if arr[j] > arr[j+1]:
                        arr[j], arr[j+1] = arr[j+1], arr[j]
        print("iteration %d:"%(i+1), *arr)
arr = [int(i) for i in input("Array: ").split(" ")]
# arr= [5, 3, 1, 2, 10, 7, 9]
odd_even_sort(arr)
print("Sorted:", *arr)
