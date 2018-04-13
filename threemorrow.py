"""Inspired by https://github.com/madisonmay/Tomorrow"""
import threading
import functools
import time
from queue import Queue


def thread(q, fn, results):
    while True:
        item = q.get()
        if item is None:
            break
        args, kwargs = item
        result = fn(*args, **kwargs)
        q.task_done()
        results.put((result, args, kwargs))

class ThreadFunction:
    def __init__(self, fn, max_threads=5):
        self.queue = Queue()
        self.results = Queue()
        self.fn = fn
        self.started = False
        self.threads = []
        self.max_threads = max_threads
    def __call__(self, *args, **kwargs):
        self.queue.put((args, kwargs))
    def __iter__(self):
        # start threads?
        for i in range(self.max_threads):
            t = threading.Thread(target=thread, args=(self.queue, self.fn, self.results))
            t.start()
            self.threads.append(t)
        for i in range(self.max_threads):
            self.queue.put(None)  # tell threads to die after completion
        return self
    def __next__(self):
        if self.results.empty() and self.queue.empty():
            raise StopIteration
        else:
            result = self.results.get()
            self.results.task_done()
            return result

def threads(howmany):
    def decorator(fn):
        return ThreadFunction(fn, howmany)
    return decorator

# Usage:
if __name__ == '__main__':
    @threads(5)
    def download(url):
        print("Sleeping 3 seconds ({})".format(url))
        time.sleep(3)
        return "result from " + url

    print("defined download")

    for url in "abcde":
        print("scheduling download of", url)
        download(url)  # just adds the call to a queue

    print("All scheduled")
    for result, args, kwargs in download:  # actually get stuff from threads
        print(args[0], "resulted in", result)
