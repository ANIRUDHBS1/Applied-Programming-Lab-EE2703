import multiprocessing as mp
import asyncio
import time
import datetime

def fib(n):
    if n <= 1: return 1
    else: return fib(n-1) + fib(n-2)

def print_fib(n):
    start = datetime.datetime.now()
    x = fib(n)
    end   = datetime.datetime.now()
    duration = end - start
    print(f"fib({n}) = {x}.  Took {duration} s.")

def main():

    x = [15, 35, 36, 37, 40, 42, 41, 39]
    f = [None]*len(x)
    t = [None]*len(x)
    # for i in range(len(x)):
    #     print_fib(x[i])
    for i in range(len(x)):
        t[i] = mp.Process(target=print_fib, args=(x[i],))
        t[i].start()

    for p in t:
        p.join()

if __name__ == '__main__':
    main()
