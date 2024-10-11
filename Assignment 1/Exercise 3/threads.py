import threading
import time
import random

def thread_work(threadid):

    print(f"Hi, I’m thread {threadid}")
    
    # This will generate integer between 1 and 5 seconds which will be assigned to each thread for sleeping
    sleeping_time = random.randint(1, 5)
    time.sleep(sleeping_time)
    # print(sleeping_time)
    print(f"Thread {threadid} says goodbye after {sleeping_time} seconds")

threads = []
for i in range(1, 4):
    thread = threading.Thread(target=thread_work, args=(i,))
    threads.append(thread)

for thread in threads:
    thread.start()


