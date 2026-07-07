from queue import Queue
from threading import Thread, Lock
from urllib.parse import urlparse

def crawl(start_url: str, html_parser) -> list[str]:
    start_host = urlparse(start_url).netloc

    queue = Queue()
    queue.put(start_url)

    visited = set([start_url])
    result = []
    lock = Lock()

    def worker():
        while True:
            url = queue.get()

            if url is None:
                queue.task_done()
                break

            with lock:
                result.append(url)

            for next_url in html_parser.get_urls(url):
                if urlparse(next_url).netloc != start_host:
                    continue

                with lock:
                    if next_url in visited:
                        continue

                    visited.add(next_url)
                    queue.put(next_url)

            queue.task_done()

    workers = []
    number_of_workers = 5

    for _ in range(number_of_workers):
        t = Thread(target=worker)
        t.start()
        workers.append(t)

    queue.join()

    for _ in range(number_of_workers):
        queue.put(None)

    for t in workers:
        t.join()

    return result

#use a shared thread-safe queue as the URL frontier and multiple crawler workers. 
#Since URL fetching is I/O-bound, concurrency improves throughput. 
#The visited set must be protected by a lock or replaced by an atomic distributed store like Redis SETNX. Each worker fetches one URL, 
#extracts links, normalizes them, checks domain rules, and atomically check-and-adds unseen URLs before pushing them back into the queue. 
#At larger scale, I would shard the queue and use distributed deduplication.


