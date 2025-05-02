#student name: Bryan zhang
#student number: 69238335

import multiprocessing
import random
import time

def philosopher(id: int, chopstick: list):
    """
        implements a thinking-eating philosopher with asymmetric chopstick acquisition.
        id is used to identifier philosopher #id (id is between 0 to numberOfPhilosophers-1)
        chopstick is the list of semaphores associated with the chopsticks
    """
    def eatForAWhile():
        print(f"DEBUG: philosopher{id} eating")
        time.sleep(round(random.uniform(.1, .3), 2))

    def thinkForAWhile():
        print(f"DEBUG: philosopher{id} thinking")
        time.sleep(round(random.uniform(.1, .3), 2))

    for _ in range(6):
        leftChopstick = id
        rightChopstick = (id + 1) % 5

        if id % 2 != 0:  # Odd philosopher: right then left
            first_chopstick = leftChopstick
            second_chopstick = rightChopstick
        else:  # Even philosopher: left then right
            first_chopstick = rightChopstick
            second_chopstick = leftChopstick

        chopstick[first_chopstick].acquire()
        print(f"DEBUG: philosopher{id} has chopstick{first_chopstick}")
        chopstick[second_chopstick].acquire()
        print(f"DEBUG: philosopher{id} has chopstick{second_chopstick}")

        eatForAWhile()

        chopstick[second_chopstick].release()
        print(f"DEBUG: philosopher{id} is to release chopstick{second_chopstick}")
        chopstick[first_chopstick].release()
        print(f"DEBUG: philosopher{id} is to release chopstick{first_chopstick}")

        thinkForAWhile()

if __name__ == "__main__":
    semaphoreList = list()
    numberOfPhilosophers = 5

    for i in range(numberOfPhilosophers):
        semaphoreList.append(multiprocessing.Semaphore(1))

    philosopherProcessList = list()
    for i in range(numberOfPhilosophers):
        philosopherProcessList.append(multiprocessing.Process(target=philosopher, args=(i, semaphoreList)))
    for j in range(numberOfPhilosophers):
        philosopherProcessList[j].start()
    for k in range(numberOfPhilosophers):
        philosopherProcessList[k].join()