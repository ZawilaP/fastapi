def synchronized():
    pass
lock=0

@classmethod
@synchronized(lock)
def foo(cls):
    pass
foo = synchronized(lock)(foo)
foo = classmethod(foo)
