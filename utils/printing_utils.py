import time

def print_time(f, *args):
  print("time for: " + f.__name__)
  start_time = time.time()
  return_val = f(*args)
  print(time.time() - start_time)
  return return_val