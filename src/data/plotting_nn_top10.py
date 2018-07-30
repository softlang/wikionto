from pandas import DataFrame, Series
from data import DATAP
from json import load
import matplotlib.pyplot as plt

f = open(DATAP + '/nndict.json', 'r', encoding="UTF8")
nndict = load(f)
f.close()
df = DataFrame(columns=['#articles'], index=nndict['NN'].keys())
for word in nndict['NN']:
    freq = nndict['NN'][word]
    df.loc[word] = Series({'#articles': freq})

df = df[df['#articles'] > 0].sort_values(by='#articles')
print(df)
ax = df.tail(10).plot(y="#articles", kind='barh', color='royalblue', fontsize=14)
ax.legend(prop={'size': 14})
plt.show()

