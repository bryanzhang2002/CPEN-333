import threading, time
    
def worker(printers):
    with printers:
        print(f"Thread {threading.current_thread().name} can print")
        time.sleep(1.5)

if __name__ == "__main__":
    printers = threading.Semaphore(3) #3 printers
    for i in range(10):
        threading.Thread(target=worker, args=(printers,)).start()
        print(printers._value)