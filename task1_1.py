
# coding: utf-8

# In[ ]:


import urllib
import urllib2
import re
import pandas
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from pandas.core.frame import DataFrame
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# In[ ]:


#get the requst from url
def get(url):
    driver = webdriver.PhantomJS()
    driver.get(url)
    time.sleep(1)
    driver.switch_to.frame("smsg")
    content = driver.page_source.encode('utf-8')
    return content


# In[ ]:


#transform the page to dataframe
def get_dtframe(page_str):
    
    bs = BeautifulSoup(page_str, "html.parser")
    table = bs.find_all('table')
    tr = table[0].find_all('tr')
    '''
        the first table
    '''
    final = []
    for cnt in tr:
        td = cnt.find_all('td')
        temp = []
        for cntt in td:
            temp.append(cntt.string)
        final.append(temp)
    colHead = final[1]
    final = final[2:]
    table_of_Data = DataFrame(final, columns=colHead)
    
    '''
        the second table
    '''
    final = []
    tr = table[1].find_all('tr')
    for cnt in tr:
        td = cnt.find_all('td')
        temp = []
        for cntt in td:
            temp.append(cntt.string)
        final.append(temp)
    colHead = final[0]
    final = final[1:]
    table_Of_End = DataFrame(final,columns = colHead)
    table_Of_End.to_csv('Data_Of_Footer.csv',encoding="utf-8")
    
    return table_of_Data


# In[ ]:


#different strategy of sorting the dataframe
def Data_Sort(dtframe, colHead, col):
    for i in range(len(dtframe[colHead[col]])):
        if str(dtframe[colHead[col]][i]) == 'None':
            dtframe[colHead[col]][i] = '0'
        dtframe[colHead[col]][i] = float(dtframe[colHead[col]][i])

    dtframe = dtframe.sort_values(by=colHead[col])
    return dtframe

#each kind of metal create a csv
def metal_to_csv(dtframe,metal_name):
    Head = dtframe.columns.values.tolist()
    dtframe = dtframe.loc[table[Head[0]].str.contains(metal_name)]
    dtframe.to_csv("metal_"+metal_name+"_data.csv",encoding="utf-8")


# In[ ]:


#plot the graph
def plot_graph(metal):
    metal = "metal_"+metal+"_data.csv"
    data = pd.read_csv(metal)

    colHead = data.columns.values.tolist()

    data[colHead[3]].plot()
    plt.title('up and down price')
    plt.show()
    data[colHead[9]].plot()
    plt.title('open_price')
    plt.show()
    data[colHead[10]].plot()
    plt.title('lowest')
    plt.show()
    data[colHead[11]].plot()
    plt.title('highest')
    plt.show()
    
def totalfunc(url):
    data = pd.read_csv(url)

    colHead = data.columns.values.tolist()
    #print type(data[colHead[1]][1])
    #data[colHead[3]]
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


# In[ ]:


if __name__ == "__main__":
    url = 'http://www.shfe.com.cn/statements/dataview.html?paramid=delaymarket_all'
    page_str = get(url)
    table = get_dtframe(page_str)
    colHead = table.columns.values.tolist()
    
    table.sort_values(by=colHead[0])
    
    table_list = ["涨跌.csv","成交量.csv","开盘.csv","最低.csv","最高.csv"]
    #sort
    tableOfUD = Data_Sort(table,colHead,2)
    tableOfUD.to_csv(table_list[0],encoding="utf-8")
    
    #table1 = table.loc[table[colHead[5]].notnull()]
    tableOfVT = Data_Sort(table,colHead,5)
    tableOfVT.to_csv(table_list[1],encoding="utf-8")
    
    #select
    tableOfKP = table.loc[table[colHead[8]].notnull()]
    tableOfKP.to_csv(table_list[2],encoding="utf-8")

    tableOfL = table.loc[table[colHead[9]].notnull()]
    tableOfL.to_csv(table_list[3],encoding="utf-8")
    
    
    tableOfH = table.loc[table[colHead[10]].notnull()]
    tableOfH.to_csv(table_list[4],encoding="utf-8")

    #each type of the metal create a csv
    metal_list = ["ag","al","au","bu","cu","fu","hc","ni","pb","rb","ru","sn","wr","zn"]
    for metal_name in metal_list: 
        metal_to_csv(table,metal_name)
        
    #plot the graph
    for metal_name in metal_list: 
        plot_graph(metal_name)
        
    totalfunc(table_list[2])
