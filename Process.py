from multiprocessing import Process, Queue, cpu_count

POOL_BATCH_RESULT = "POOL_BATCH_RESULT"

class Pool:
    def __init__(self, nprocesses = None, debug = False):
        self._nprocesses = nprocesses if not nprocesses in [None, 0] else cpu_count()
        self._processes = []
        self._results = Queue()
        self._debug = debug
        return

    def AddTask(self, fn, *args, **kwargs):
        process = Process(target=self._fn_wrapper, args=[fn, self._results, args, kwargs])
        self._processes.append(process)
        return

    def AddTaskBatch(self, fn, listargs):

        num_list_args = len(listargs)
        if num_list_args == 0: return

        num_processes = self._nprocesses
        if self._nprocesses > num_list_args: num_processes = num_list_args

        num_items_per_process = self._nprocesses if self._nprocesses < num_list_args else num_list_args

        num_items_per_process = num_list_args // num_processes
        num_items_left = num_list_args % num_processes

        segments = []
        for i in range(0, num_processes):
            start = i * num_items_per_process
            stop  = start + num_items_per_process
            segments.append(stop)

        idx_segment_head_for_combination = len(segments) - num_items_left

        if num_items_left > 0:
            for i, _ in enumerate(segments[idx_segment_head_for_combination:]):
                segments[i + idx_segment_head_for_combination] += i + 1
        del segments[-1]
        segments.insert(0, 0)

        if self._debug: print(f"Summary:"
                              f"\n\t{num_list_args} items"
                              f"\n\t{num_processes} processes"
                              f"\n\t{num_items_per_process} items per process"
                              f"\n\t{num_items_left} items are combined to last {num_items_left} processes"
                              f"\n\tProcesses:")

        for i, segment in enumerate(segments):

            start = segments[i]
            stop  = segments[i + 1] if i < num_processes - 1 else None

            batch_args = listargs[start:stop]

            if self._debug: print(f"\t\tProcess#{i + 1}: {len(batch_args)} items")

            process = Process(target=self._fn_batch, args=[fn, self._results, batch_args])
            self._processes.append(process)

        return

    def Launch(self, autoclose = True):
        result = []

        if self._debug: print(f"\t{len(self._processes)} processes are created")

        for process in self._processes: process.start()

        for process in self._processes:
            ret = self._results.get()
            if type(ret) is dict and POOL_BATCH_RESULT in ret.keys():
                result.extend(ret[POOL_BATCH_RESULT])
            else: result.append(ret)

        for process in self._processes: process.join()

        if autoclose: self._results.close()

        if self._debug: print(f"\t{len(self._processes)} processes are terminated")

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