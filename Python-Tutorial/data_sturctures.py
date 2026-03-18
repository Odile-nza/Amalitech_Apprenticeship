import numpy as np
import pandas as pd

s = pd.Series(np.random.randn(5), index=["a", "b", "c", "d", "e"])
print(s)

print(s.index)

print (pd.Series(np.random.randn(5)))

d = {"b":1, "a":0, "c":2}
print(pd.Series(d))

f = pd.Series(d, index=["b", "c", "d","a"])
print(f)

#Slice
print(s.iloc[0])
print(s.iloc[:3])

#median
print (s[s > s.median()])

print(s.iloc[[4,3,1]])

#exponential
print (np.exp(s))

print(s.dtype)

#actual array
print(s.array)

#actual ndarray
print(s.to_numpy)

#series as dict
print(s["a"])
s["e"]=12
print(s)

print ("e" in s)
print('f' in s)

#series.get
s.get("f")
print(s)
print(s.get("f", np.nan))

#Name attribute
s = pd.Series(np.random.randn(5), name="something")
print(s)

print(s.name)

s2= s.rename("different")
print(s2.name)

#DataFrame
d ={
    "one": pd.Series([1.0,2.0,3.0], index=["a","b","c"]),
    "two": pd.Series([1.0,2.0,3.0,4.0], index=["a","b","c","d"]),
}

df = pd.DataFrame(d)

print(df)

print(pd.DataFrame(d, index=["d","b","a"]))

print(pd.DataFrame(d, index=["d","b","a"], columns=["two","three"]))

#From dict of ndarrays / lists
d = {"one": [1.0,2.0,3.0,4.0], "two": [4.0,3.0,2.0,1.0]}
print(pd.DataFrame(d))
print(pd.DataFrame(d, index=["a","b","c","d"]))

#From structured or record array
data = np.zeros((2,),dtype=[("A","i4"),("B","f4"),("C","S10")])#create an array with **2 empty slots**, filled with zeros initially.
data[:] = [(1,2.0,"Hello"), (2,3.0,"World")] #a common NumPy slicing pattern.
print(pd.DataFrame(data))
print(pd.DataFrame(data, index=["first", "second"]))
print(
pd.DataFrame(data, columns=["C", "A", "B"]))

#from a series
ser = pd.Series(range(3), index=list("abc"), name="ser")
print(pd.DataFrame(ser))

#From a list of namedtuples
from collections import namedtuple

Point = namedtuple("Point", "x y")
print(pd.DataFrame([Point(0,0),Point(0,3),Point(2,3)]))

#From a list of dataclasses
from dataclasses import make_dataclass

Point = make_dataclass("Point", [("x", int), ("y", int)])

print(pd.DataFrame([Point(0,0),Point(0,3),Point(2,3)]))

#Alternate constructors
print(pd.DataFrame.from_dict(dict([("A",[1,2,3]), ("B", [4,5,6])])))

print( pd.DataFrame.from_dict(
    dict([("A",[1,2,3]), ("B", [4,5,6])]),
    orient="index",
    columns=["one", "two", "three"],
))

#Column selection, addition, deletion
print(df["one"])
df["three"] = df["one"] * df["two"]
df["flag"] = df["one"] >2

print(df)