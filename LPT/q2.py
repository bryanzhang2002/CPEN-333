import threading
import random

BUFFER_SIZE = 5
NUM_READS = 3
NUM_PRODUCE = 5

buffer = [0] * BUFFER_SIZE
read_ptr = 0
write_ptr = 0
item_count = 0

buffer_lock = threading.Lock()
empty_slots = threading.Semaphore(BUFFER_SIZE)
full_slots = threading.Semaphore(0)

def reader():
    global item_count, read_ptr #Added read_ptr
    for _ in range(random.randint(1, NUM_READS)):
        buffer_lock.acquire()
        if item_count > 0:
            full_slots.acquire()
            item = buffer[read_ptr]
            print(f"Reader {threading.current_thread().name} read: {item}")
            read_ptr = (read_ptr + 1) % BUFFER_SIZE
            item_count -= 1
            full_slots.release()
            empty_slots.release()
        buffer_lock.release()
        threading.Event().wait(random.uniform(0.1, 0.5))

def producer():
    global item_count, write_ptr #Added write_ptr
    for _ in range(NUM_PRODUCE):
        empty_slots.acquire()
        buffer_lock.acquire()
        item = random.randint(1, 100)
        buffer[write_ptr] = item
        print(f"Producer produced: {item}")
        write_ptr = (write_ptr + 1) % BUFFER_SIZE
        item_count += 1
        buffer_lock.release()
        full_slots.release()
        threading.Event().wait(random.uniform(0.1, 0.5))

def consumer():
    global item_count, read_ptr #Added read_ptr
    for _ in range(NUM_PRODUCE):
        buffer_lock.acquire()
        if item_count > 0:
            full_slots.acquire()
            item = buffer[read_ptr]
            print(f"Consumer consumed: {item}")
            read_ptr = (read_ptr + 1) % BUFFER_SIZE
            item_count -= 1
            full_slots.release()
            empty_slots.release()
        buffer_lock.release()
        threading.Event().wait(random.uniform(0.1, 0.5))

if __name__ == "__main__":
    readers = [threading.Thread(target=reader, name=f"Reader-{i}") for i in range(3)]
    producer_thread = threading.Thread(target=producer, name="Producer")
    consumer_thread = threading.Thread(target=consumer, name="Consumer")

    for reader_thread in readers:
        reader_thread.start()
    producer_thread.start()
    consumer_thread.start()

    for reader_thread in readers:
        reader_thread.join()
    producer_thread.join()
    consumer_thread.join()

    print("All threads finished.")