# Nicely formatted time string
import time


def hms_string(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)


def start_time():
    return time.time()


def stop_time(start_time):
    print(hms_string(time.time() - start_time))