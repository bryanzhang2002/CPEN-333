
import threading


class Buffer():
    def __init__(self, size):
        self.queue = [None]*size
        self.front = 0
        self.back = 0
    
    def pop(self)->int:
        # remove element from front
        temp = self.queue[self.front]
        self.queue[self.front] = None
        self.front = (self.front + 1) % SIZE
        return temp

    def push(self, item: int)->None:
        self.queue[self.back] = item
        self.back = (self.back + 1) % SIZE
        return None
    
    def peek(self)->None:
        return self.queue[self.back-1] # just peeking into back

    

def reader():
    for _ in range(5):
        print(f"read: {circularBuffer.peek()}")    


def consumer():
    for _ in range(5):
        bufferFull.acquire()
        writingLock.acquire()
        print(f"popped: {circularBuffer.pop()}", end="")
        print(" ", circularBuffer.queue)
        bufferEmpty.release()
        writingLock.release()
    

def producer():
    for item in range(5):
        bufferEmpty.acquire()
        writingLock.acquire()
        circularBuffer.push(item)
        print(f"pushed: {item}", end="")
        print(" ", circularBuffer.queue)
        bufferFull.release()
        writingLock.release()
    

if __name__ == "__main__":
    # so we don't check for fullness, we use semaphores for that 
    SIZE = 5
    circularBuffer = Buffer(SIZE)

    bufferEmpty = threading.Semaphore(SIZE)
    bufferFull = threading.Semaphore(0)
    
    writingLock = threading.Lock() # to eliminate race condition from producer/consumer

    threadList = []

    for i in range(3):
        threadList.append(threading.Thread(name =f"reader{i}", target=reader))


    threadList.append(threading.Thread(name="producer", target=producer))
    threadList.append(threading.Thread(name="consumer", target=consumer))

    for x in threadList:
        x.start()

    # all are non-daemonic so we don't need to use join()
