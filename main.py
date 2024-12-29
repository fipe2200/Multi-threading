from threading import Thread, Lock, Semaphore
import time

global_string = ""

locker = Semaphore(3)
waithall = Lock()

class write_to_string(Thread):
    def run(self):
        global global_string
        for L in range(5):

            # Måste ha en väntzon pga race
            with waithall:
                for _ in range(3):
                    locker.acquire()

            # Kritisk zon
            if self.getName() == "Thread-1":
                global_string = time.strftime("%Y-%m-%d %H:%M:%S") + " Milli:" + str(
                    round(time.time() * 1000) % 1000)
            else:
                global_string = time.strftime(
                    " Milli:" + str(round(time.time() * 1000) % 1000) + " %S-%M-%H %d:%m:%Y")

            print(self.getName() + " Enters write critical zone\n", end="")
            print(self.getName() + " Writes:" + global_string + "\n", end="")
            print(self.getName() + " left write critical zone\n", end="")

            locker.release(3)


class read_from_string(Thread):
    def run(self):
        global global_string
        for L in range(5):

            # Måste ha en väntzon pga race
            with waithall:
                locker.acquire()

            # kritisk zon
            print(self.getName() + " Enters read critical \n", end="")
            print(self.getName() + " Reading from string Date:" + global_string + "\n", end="")
            print(self.getName() + " left read critical zone \n", end="")

            locker.release()

threads = []

# writers
for i in range(2):
    w = write_to_string()
    threads.append(w)
    w.start()

# Readers
for j in range(3):
    r = read_from_string()
    threads.append(r)
    r.start()

for t in threads:
    t.join()
