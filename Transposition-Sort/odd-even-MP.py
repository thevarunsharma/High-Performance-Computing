import multiprocessing as mp

def compare(arr, idx):
    if idx < len(arr)-1 and arr[idx] > arr[idx+1]:
        arr[idx], arr[idx+1] = arr[idx+1], arr[idx]

def odd_even_sort(arr):
    n = len(arr)
    for i in range(len(arr)):
        if i & 1 == 0:
            pool = mp.Pool(mp.cpu_count())
            [pool.apply(compare, args=(arr, j)) for j in range(0, n-1, 2)]
            pool.close()
        else:
            pool = mp.Pool(mp.cpu_count())
            [pool.apply(compare, args=(arr, j)) for j in range(1, n-1, 2)]
            pool.close()
        print("iteration %d:"%(i+1), *arr)
arr = [int(i) for i in input("Array: ").split(" ")]
# arr= [5, 3, 1, 2, 10, 7, 9]
odd_even_sort(arr)
print("Sorted:", *arr)
