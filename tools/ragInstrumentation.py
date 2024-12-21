"""
This module provides a decorator to measure the execution time of functions.
This module provides a decorator to log query into database.

"""
import time

DEBUG = False

def measure_execution_time(func):
    """
    Decorator that measures the execution time of a function.

    Args:
        func (callable): The function to be measured.

    Returns:
        callable: The wrapped function with execution time measurement.

    Example:
        @measure_execution_time
        def my_function():
            # function implementation
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # convert to milliseconds
        if DEBUG: print(f"Execution time of {func.__name__}: {execution_time:.2f} ms")
        return result
    return wrapper

# example
# @measure_execution_time
# def summy(*args, **kwargs):
#     time.sleep(1)  # Simulate a time-consuming operation
#     return sum(args) + sum(kwargs.values())

# # Example usage
# result = summy(5, 3, a=2, b=4)
# print(f"Result: {result}")

def log_query(func):
    """
    Decorator that inserts the LLM query into a database, if the DEBUG flag is set to True.

    Args:
        func (callable): The function to be measured.

    Returns:
        callable: The wrapped function.

    Example:
        @log_query
        def my_function():
            # function implementation
    """
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        fn = func.__name__
        a = list(args)
        with open("query_log.txt", "a") as logfile:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            logfile.write(f"{current_time} - Function: {func.__name__}\n")
            logfile.write(f"  Result: {result}\n")
            logfile.write(f"  Params: {a}\n")
        if DEBUG: 
            print(fn)
            #print(f"{fn},  Params: {a},Result: {result}")
        return result
    return wrapper

