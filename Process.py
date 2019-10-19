from multiprocessing import Process, Queue, cpu_count

POOL_BATCH_RESULT = "POOL_BATCH_RESULT"

class Pool:
    def __init__(self, nprocesses = None):
        self._nprocesses = nprocesses if not nprocesses in [None, 0] else cpu_count()
        self._processes = []
        self._results = Queue()
        return

    def AddTask(self, fn, *args, **kwargs):
        process = Process(target=self._fn_wrapper, args=[fn, self._results, args, kwargs])
        self._processes.append(process)
        return

    def AddTaskBatch(self, fn, listargs):

        num_list_args = len(listargs)
        if num_list_args == 0: return

        num_items_per_batch = self._nprocesses if self._nprocesses < num_list_args else num_list_args

        num_processes = num_list_args // num_items_per_batch
        if num_list_args % num_items_per_batch != 0: num_processes += 1

        for i in range(0, num_list_args, num_items_per_batch):
            batch_args = listargs[i : i + num_items_per_batch]
            process = Process(target=self._fn_batch, args=[fn, self._results, batch_args])
            self._processes.append(process)

        return

    def Launch(self, autoclose = True):
        result = []

        for process in self._processes: process.start()

        for process in self._processes:
            ret = self._results.get()
            if type(ret) is dict and POOL_BATCH_RESULT in ret.keys():
                result.extend(ret[POOL_BATCH_RESULT])
            else: result.append(ret)

        for process in self._processes: process.join()

        if autoclose: self._results.close()

        return result

    @staticmethod
    def _fn_wrapper(fn, result, args, kwargs):
        ret = fn(*args, **kwargs)
        result.put(ret)

    @staticmethod
    def _fn_batch(fn, results, batchargs):
        result = []
        for args in batchargs:
            ret = fn(*args)
            result.append(ret)
        results.put({ POOL_BATCH_RESULT: result })

# Eg.

# from PyVutils import Process

# def task(v1, v2, v3):
#     print(f"task({v1}, {v2}, {v3})")
#     for v in range(0, 10000000): pass
#     return [v1, v2, v3]

# if __name__ == "__main__":
#     pool = Process.Pool()
#     pool.AddTaskBatch(task, [(i, i, i) for i in range(0, 14)])
#     result = pool.Launch()
#     print(result)