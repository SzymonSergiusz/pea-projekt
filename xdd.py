import time
from time import perf_counter

start = perf_counter()
time.sleep(5)
stop = perf_counter()
print(stop-start)