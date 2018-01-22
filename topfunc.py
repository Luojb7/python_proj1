
# coding: utf-8

# In[57]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
def totalfunc(url):
    data = pd.read_csv(url)

    colHead = data.columns.values.tolist()
    #print type(data[colHead[1]][1])
    #data[colHead[3]]

    '''
    print data[colHead[3]].min()
    print data[colHead[3]].max()
    print data[colHead[3]].mean()
    print data[colHead[3]].var()
    '''
    data[colHead[3]].plot(kind='bar')
    plt.title('up and down price')
    plt.show()
    data[colHead[9]].plot(kind='bar')
    plt.title('open_price')
    plt.show()
    data[colHead[10]].plot(kind='bar')
    plt.title('lowest')
    plt.show()
    data[colHead[11]].plot(kind='bar')
    plt.title('highest')
    plt.show()

if __name__ == "__main__":
     url = "开盘.csv"
     totalfunc(url)

