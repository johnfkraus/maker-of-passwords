import functools
import pandas as pd

def tracefunc(func):
    """Decorates a function to show its trace."""

    @functools.wraps(func)
    def tracefunc_closure(*args, **kwargs):
        """The closure."""
        result = func(*args, **kwargs)
        print(f"{func.__name__}(args={args}, kwargs={kwargs}) => {result}")
        return result

    return tracefunc_closure


df1 = pd.DataFrame({'temp_c': [17.0, 25.0]},
	                  index=['Portland', 'Berkeley'])

df2 = pd.DataFrame({'humidity_rh': [85, 65]},
	                  index=['Portland', 'Berkeley'])

print(tracefunc(pd.merge)(df1, df2, left_index=True, right_index=True))
