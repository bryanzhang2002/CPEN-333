#student name: Bryan Zhang
#student number: 69238335

import threading

def sortingWorker(firstHalf: bool) -> None:
    """
       If param firstHalf is True, the method
       takes the first half of the shared list testcase,
       and stores the sorted version of it in the shared 
       variable sortedFirstHalf.
       Otherwise, it takes the second half of the shared list
       testcase, and stores the sorted version of it in 
       the shared variable sortedSecondHalf.
       The sorting is ascending and is implemented by bubble sort.
    """
    mid = len(testcase) // 2

    def bubble_sort(arr):
        # Bubble sort implementation
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

    if firstHalf:
        sortedFirstHalf[:] = bubble_sort(testcase[0:mid])
    else:
        sortedSecondHalf[:] = bubble_sort(testcase[mid:len(testcase)])

def mergingWorker() -> None:
    """ This function uses the two shared variables 
        sortedFirstHalf and sortedSecondHalf, and merges/sorts
        them into a single sorted list that is stored in
        the shared variable sortedFullList.
    """
    global sortedFirstHalf, sortedSecondHalf, SortedFullList
    i: int = 0
    j: int = 0
    n: int = len(sortedFirstHalf)

    
    while i < n and j < n:
        if sortedFirstHalf[i] < sortedSecondHalf[j]:    # if an element is less than its corresponding element in the other half, append that one first
            SortedFullList.append(sortedFirstHalf[i])
            i += 1 
        else:
            SortedFullList.append(sortedSecondHalf[j])
            j += 1

    # Append remaining elements one by one
    while i < n:
        SortedFullList.append(sortedFirstHalf[i])
        i += 1

    while j < n:
        SortedFullList.append(sortedSecondHalf[j])
        j += 1

if __name__ == "__main__":
    #shared variables
    testcase = [8,5,7,7,4,1,3,2]
    sortedFirstHalf: list = []
    sortedSecondHalf: list = []
    SortedFullList: list = []
    
    # initiate and start sorting threads 
    sort1 = threading.Thread(target=sortingWorker, args=(True,))
    sort2 = threading.Thread(target=sortingWorker, args=(False,))

    sort1.start()
    sort2.start()

    # Wait for sorting to complete
    sort1.join()
    sort2.join()

    # Merge sorted halves
    merge = threading.Thread(target=mergingWorker)
    merge.start()
    merge.join()

    #as a simple test, printing the final sorted list
    print("The final sorted list is ", SortedFullList)