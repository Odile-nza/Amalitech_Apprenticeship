import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

iris = pd.read_csv(
    "data/iris.data.txt",
    names=["SepalLength", "SepalWidth", "PetalLength", "PetalWidth", "Name"]
)

#Assigning new columns in method chains
print(iris.head())

print (
    iris.assign(sepal_ratio=iris["SepalWidth"] / iris["SepalLength"]).head()
)

#pass in a function of one argument to be evaluated on the DataFrame being assigned to
print(
    iris.assign(sepal_ratio=lambda x: (x["SepalWidth"] / x["SepalLength"])).head()
)

#usinf pandas.col()
print(
    iris.assign(sepal_ration=pd.col("SepalWidth") / pd.col("SepalLength")).head()
)

#we can limit the DataFrame to just those observations with a Sepal Length greater than 5, calculate the ratio, and plot
(
    iris.query("SepalLength >5")
    .assign(
        SepalRatio = lambda  x: x.SepalWidth / x.SepalLength,
        PetalRatio = lambda x: x.PetalWidth / x.PetalLength,
    )
    .plot(kind="scatter", x="SepalRatio", y="PetalRatio")
)
#plt.show()