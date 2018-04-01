
class CrawlQueue(object):
    thread_pools = []

    def __init__(self, pool_size=5):
        self.pool_size = pool_size

    def put_queue(self, thread):
        if len(self.thread_pools) == self.pool_size:
            return False
        self.thread_pools.append(thread)
        return True

    def pop_queue(self, thread_name):
        remove_thread = None
        for thread in self.thread_pools:
            if thread.name <> thread_name:
                continue
            remove_thread = thread
        if remove_thread is not None:
            self.thread_pools.remove(remove_thread)

