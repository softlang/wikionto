import matplotlib.pyplot as plt
from data import DATAP
from json import load
from pandas import DataFrame

with open(DATAP+"/feature_freq.json", "r") as f:
    freq = load(f)
    freq = [(key, value) for key, value in freq.items() if value > 10]
    print(len(freq))
df = DataFrame.from_records(freq, columns=["Title", "Freq"])
df = df.sort_values(by='Freq')
print(df)
ax = df.plot(x="Title", y="Freq", logy=True)
ax.set_title('Feature Frequency')
plt.show()