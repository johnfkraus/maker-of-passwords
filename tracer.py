import functools


def tracefunc(func):
    """Decorates a function to show its trace."""

    @functools.wraps(func)
    def tracefunc_closure(*args, **kwargs):
        """The closure."""
        result = func(*args, **kwargs)
        print(f"{func.__name__}(args={args}, kwargs={kwargs}) => {result}")
        return result

    return tracefunc_closure 


