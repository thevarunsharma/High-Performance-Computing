import threading

def compare(arr, idx):
    if idx < len(arr)-1 and arr[idx] > arr[idx+1]:
        arr[idx], arr[idx+1] = arr[idx+1], arr[idx]

def odd_even_sort(arr, threads):
    for i in range(len(arr)):
        if i & 1 == 0:
            for j in range(len(threads)):
                threads[j] = threading.Thread(target=compare, args=(arr, 2*j))
                threads[j].start()
            for j in range(len(threads)):
                threads[j].join()
        else:
            for j in range(len(threads)):
                threads[j] = threading.Thread(target=compare, args=(arr, 2*j+1))
                threads[j].start()
            for j in range(len(threads)):
                threads[j].join()
        print("iteration %d:"%(i+1), *arr)

arr = [int(i) for i in input("Array: ").split(" ")]
threads = [None]*((len(arr) + 1)//2)
odd_even_sort(arr, threads)
print("Sorted:", *arr)
