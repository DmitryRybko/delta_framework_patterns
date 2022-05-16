from time import time


class Debug:

    def __init__(self, name):

        self.name = name

    def __call__(self, cls):

        def timeit(method):  # timeit представляется тут излишним, см. DebugAlt ниже.

            def timed(*args, **kwargs):
                ts = time()
                result = method(*args, **kwargs)
                te = time()
                delta = te - ts

                print(f'debug --> {self.name} выполнялся {delta:2.2f} ms')
                return result

            return timed

        return timeit(cls)


class DebugAlt:

    def __init__(self, name):

        self.name = name

    def __call__(self, method):

        def timed(*args, **kwargs):
            ts = time()
            result = method(*args, **kwargs)
            te = time()
            delta = te - ts

            print(f'debug --> {self.name} выполнялся {delta:2.2f} ms')
            return result

        return timed


class DebugNew:

    def __call__(self, method):

        def timed(*args, **kwargs):
            ts = time()
            result = method(*args, **kwargs)
            te = time()
            delta = te - ts

            print(f'debug --> {method} выполнялся {delta:2.2f} ms')
            return result

        return timed
