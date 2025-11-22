import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.DataFrame({"col1": [1, 2, 3]})
df

x = 10
"x", x

arr = np.random.normal(1, 1, size=100)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)
fig