from multiprocessing import Process, Lock

import time


class Monitor():
    lock = Lock()

    def foo(self, tid):
        with Monitor.lock:
            print("{} in foo".format(tid))
            time.sleep(3)

    def ker(self, tid):
        with Monitor.lock:
            print("{} in ker".format(tid))


m = Monitor()

def task1(id):
    m.foo(id)

def task2(id):
    m.ker(id)


p1 = Process(target=task1, args=(1,))
p2 = Process(target=task2, args=(2,))

p1.start()
p2.start()

p1.join()
p2.join()
