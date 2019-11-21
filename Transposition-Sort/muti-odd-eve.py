from multiprocessing import Process, Array

def compare(arr, idx):
    if idx < len(arr)-1 and arr[idx] > arr[idx+1]:
        arr[idx], arr[idx+1] = arr[idx+1], arr[idx]

def odd_even_sort(arr, process):
    for i in range(len(arr)):
        if i & 1 == 0:
            for j in range(len(process)):
                process[j] = Process(target=compare, args=(arr, 2*j))
                process[j].start()
            for j in range(len(process)):
                process[j].join()
        else:
            for j in range(len(process)):
                process[j] = Process(target=compare, args=(arr, 2*j+1))
                process[j].start()
            for j in range(len(process)):
                process[j].join()
        print("iteration %d:"%(i+1), *arr)

arr = [int(i) for i in input("Array: ").split(" ")]
arr = Array('i', arr)
process = [None]*((len(arr) + 1)//2)
odd_even_sort(arr, process)
print("Sorted:", *arr)
