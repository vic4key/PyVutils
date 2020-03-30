from multiprocessing import Process, Queue, cpu_count

POOL_BATCH_RESULT = "POOL_BATCH_RESULT"

class Pool:
    def __init__(self, nprocesses = None, debug = False):
        self._debug = debug
        self._fn = None
        self._tasks = []
        self._results = Queue()
        processes = []
        self._nprocesses = nprocesses if not nprocesses in [None, 0] else cpu_count()
        return

    def AddTask(self, fn, args):
        self._fn = fn
        self._tasks.append(args)
        return

    def AddTaskBatch(self, fn, listargs):
        self._fn = fn
        self._tasks.extend(listargs)
        return

    def Launch(self, autoclose = True):

        # distribute tasks to each process

        num_list_args = len(self._tasks)
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

        # balance tasks in all process

        idx_segment_head_for_combination = len(segments) - num_items_left

        if num_items_left > 0:
            for i, _ in enumerate(segments[idx_segment_head_for_combination:]):
                segments[i + idx_segment_head_for_combination] += i + 1
        del segments[-1]
        segments.insert(0, 0)

        # summary tasks

        if self._debug: print(
            ("Summary:") +
            ("\n\t%d items" % num_list_args) +
            ("\n\t%d processes" % num_processes) +
            ("\n\t%d items per process" % num_items_per_process) +
            ("\n\t%d items are combined to last %d processes" % (num_items_left, num_items_left)) +
            ("\n\tProcesses:"))

        # assign tasks to each process

        processes = []

        for i, segment in enumerate(segments):

            start = segments[i]
            stop  = segments[i + 1] if i < num_processes - 1 else None

            batch_args = self._tasks[start:stop]

            if self._debug: print("\t\tProcess#%d: %d items" % (i + 1, len(batch_args)))

            process = Process(target=self._fn_batch, args=[self._fn, self._results, batch_args])
            processes.append(process)

        # run multi-processing

        result = []

        if self._debug: print("\t%d processes are created" % len(processes))

        for process in processes: process.start()

        # combine results

        for process in processes:
            ret = self._results.get()
            if type(ret) is dict and POOL_BATCH_RESULT in ret.keys():
                result.extend(ret[POOL_BATCH_RESULT])
            else: result.append(ret)

        for process in processes: process.join()

        if autoclose: self._results.close()

        if self._debug: print("\t%d processes are terminated" % len(processes))

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
#     for v in range(0, 10000000): pass
#     return [v1, v2, v3]

# if __name__ == "__main__":
#     pool = Process.Pool(debug=True)
#     pool.AddTaskBatch(task, [(i, i, i) for i in range(0, 14)])
#     result = pool.Launch()
#     print(result)

def AdjustPrivileges(privileges, enable=True):
    # https://docs.microsoft.com/en-us/windows/win32/secauthz/privilege-constants
    import win32api, win32security
    flags = win32security.TOKEN_ADJUST_PRIVILEGES | win32security.TOKEN_QUERY
    token = win32security.OpenProcessToken(win32api.GetCurrentProcess(), flags)
    id = win32security.LookupPrivilegeValue(None, privileges)
    if enable: new_privileges = [(id, win32security.SE_PRIVILEGE_ENABLED)]
    else: new_privileges = [(id, 0)]
    win32security.AdjustTokenPrivileges(token, 0, new_privileges)
    return