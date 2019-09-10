import timeit
import pandas as pd

s = """
from homework2 import score
score("soccer.jfif", {})
"""
k = []
time = []
for i in range(2, 11):
    t = timeit.timeit(s.format(str(i)), number=5)
    print("k: {}\ntime: {}\n".format(str(i), str(t)))
    time.append(t)
    k.append(i)

time = [x / 5 for x in time]

df = pd.DataFrame({"k": k, "time": time})

