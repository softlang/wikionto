from data import DATAP
from json import load
import pandas
import matplotlib.pyplot as plt


def plot_prop_seed():
    f = open(DATAP + '/prop_seed.csv', 'r', encoding="UTF8")
    headers = ['property', '#cl-candidates', '#non-cl-candidates']
    df = pandas.read_csv(f, delimiter=',', names=headers,
                         dtype={'property': object, '#cl-candidates': int, '#non-cl-candidates': int})

    df2 = df.sort_values(by=['#non-cl-candidates', '#cl-candidates'])

    fig, axes = plt.subplots(nrows=1, ncols=3)

    df2.plot(x='property', y='#cl-candidates', style='.', color='blue', ax=axes[0])
    df2.plot(x='property', y='#non-cl-candidates', style='-', color='red', ax=axes[0])

    df2[(df2['#non-cl-candidates'] < 100)] \
        .plot(x='property', y='#cl-candidates', style='.', color='blue', ax=axes[1])
    df2[(df2['#non-cl-candidates'] < 100)] \
        .plot(x='property', y='#non-cl-candidates', style='-', color='red', ax=axes[1])
    axes[1].set_xticklabels(df2.property)

    df[(df['#cl-candidates'] > df['#non-cl-candidates']) & (df['#non-cl-candidates'] < 10000)] \
        .plot(x='#non-cl-candidates', y='#cl-candidates', style='.', color='green', ax=axes[2])
    df[(df['#non-cl-candidates'] > df['#cl-candidates']) & (df['#non-cl-candidates'] < 10000)] \
        .plot(x='#non-cl-candidates', y='#cl-candidates', style='.', color='orange', ax=axes[2])

    for ax in axes:
        ax.legend()
    plt.show()


def plot_selective_props_seed():
    f = open(DATAP + '/prop_seed.csv', 'r', encoding="UTF8")
    headers = ['property', '#cl-candidates', '#non-cl-candidates']
    df = pandas.read_csv(f, delimiter=',', names=headers,
                         dtype={'property': object, '#cl-candidates': int, '#non-cl-candidates': int})

    df1 = df.sort_values(by=['#non-cl-candidates', '#cl-candidates'])
    df2 = df1[(df1['#non-cl-candidates'] < 100)]
    ax = df2.plot(x='property', y='#cl-candidates', kind='bar', color='blue', logy=True, alpha=0.5)
    df2.plot(x='property', y='#non-cl-candidates', style='-', color='red', ax=ax, logy=True)

    ax.set_xticklabels(df2.property)
    ax.tick_params(axis='x', which='both', labelsize='small', labelcolor='black', labelrotation=-30)
    ax.legend()

    plt.show()


def to_csv_props_all():
    f = open(DATAP + '/all_props.json', 'r', encoding="UTF8")
    propdict = load(f)
    f.close()
    f = open(DATAP + '/prop_all.csv', 'w', encoding="UTF8")
    for p in propdict:
        p_in = propdict[p]["in_count"]
        p_out = propdict[p]["out_count"]
        f.write(p + '<->' + str(p_in) + '<->' + str(p_out) + '\n')
    f.flush()
    f.close()


def plot_selective_props_all():
    f = open(DATAP + '/prop_all.csv', 'r', encoding="UTF8")
    headers = ['property', '#cl-candidates', '#non-cl-candidates']
    df = pandas.read_csv(f, delimiter='<->', names=headers,
                         dtype={'property': object, '#cl-candidates': int, '#non-cl-candidates': int})

    df1 = df.sort_values(by=['#non-cl-candidates', '#cl-candidates'])
    df2 = df1[(df1['#non-cl-candidates'] < 100) & (df1['#non-cl-candidates'] < df1['#cl-candidates'])]
    ax = df2.plot(x='property', y='#cl-candidates', kind='bar', color='blue', logy=True, alpha=0.5)
    df2.plot(x='property', y='#non-cl-candidates', style='-', color='red', ax=ax, logy=True)

    ax.set_xticklabels(df2.property)
    ax.tick_params(axis='x', which='both', labelsize='small', labelcolor='black', labelrotation=-90)
    ax.legend()
    plt.show()