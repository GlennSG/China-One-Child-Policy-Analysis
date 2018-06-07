
# coding: utf-8

# In[110]:


import numpy as np
import pandas as pd


# In[111]:


# read-in world population growth data
un_data = pd.read_csv("API_SP.POP.GROW_DS2_en_csv_v2_9946255.csv",skiprows=3)
#un_data = un_data.set_index("Country Name")
display(un_data)


# In[112]:


# isolate china's population growth (1960-2016)
china_popg = un_data.loc[un_data["Country Name"] == "China"]
china_popg.head()


# In[113]:


pop_a = china_popg.iloc[:,4:23]
pop_a.index = [0]
display(pop_a.index)


# In[114]:


pop_b = china_popg.iloc[:,23:len(china_popg.columns)-2]
pop_b.index = [0]
display(pop_b.index)


# In[115]:


# add 1941 to 1959 population data to pop_a (removed for adjustment)
#old_pop_data = np.array([520843000,524139000,527456000,530795000,534154000,537534000,540936000,544359000,547804000,541670000,556613000,563000000,574820000,587960000,602660000,614479000,627393000,640629000,654159000,667964000])
#years = ["1941","1942","1943","1944","1945",1946,1947,1948,1949,1950,1951,1952,1953,1954,1955,1956,1957,1958,1959]

#years = list(range(1941,1960))
#years = [str(i) for i in years]
#def calc_pop_growth_rate(np_array):
    #return [((y-x)/x)*100 for x,y in zip(np_array,np_array[1:])]

#new_pop_data = calc_pop_growth_rate(old_pop_data)
#print(years)


# In[116]:


#new_pop_data = np.array(new_pop_data)
#df_pop_data_a = pd.DataFrame(new_pop_data.reshape(-1,len(new_pop_data)),columns=years)
#df_pop_data_a["1960"] = pop_a["1960"].values
# merge pop_a with df_pop_data_a
#pop_a = pd.merge(pop_a,df_pop_data_a).sort_index(axis=1)
#display(pop_a.index)


# In[117]:


# read-in GDP per capita data
gdp_data = pd.read_csv("average-real-gdp-per-capita-across-countries-and-regions.csv")
gdp_data.head(5)


# In[118]:


# isolate china's GDP
china_gdp = gdp_data.loc[gdp_data["Entity"] == "China"]
china_gdp = china_gdp.rename(columns={"Real GDP per capita in 2011US$, multiple benchmarks (Maddison Project Database (2018)) ($)":"Real GDP per capita"})
china_gdp.head(5)


# In[119]:


gdp_a = pd.DataFrame(columns=["Year","Avg Real GDP per capita"])
gdp_a["Year"] = pd.Series([str(i) for i in list(range(1960,1979))])
gdp_a["Avg Real GDP per capita"]= pd.Series(china_gdp.loc[((china_gdp["Year"] < 1979) & (china_gdp["Year"] > 1959)),"Real GDP per capita"].values)
#gdp_a["Avg Real GDP per capita"] = gdp_a["Avg Real GDP per capita"].shift(9)
#gdp_a["Avg Real GDP per capita"].fillna((china_gdp.loc[(china_gdp["Year"]<1940)&(china_gdp["Year"]>1928),"Real GDP per capita"].values.mean()),inplace=True)
display(gdp_a)


# In[120]:


gdp_b = pd.DataFrame(columns=["Year","Avg Real GDP per capita"])
gdp_b["Year"] = pd.Series([str(i) for i in list(range(1979,2017))])
gdp_b["Avg Real GDP per capita"]= pd.Series(china_gdp.loc[china_gdp["Year"] >= 1979,"Real GDP per capita"].values)
#gdp_b.index = [0]
display(gdp_b)


# In[121]:


# change headers into column (population growth)
def new_df(old_df,col_title):
    new_df = pd.DataFrame(columns=[col_title])
    new_df[col_title] = old_df.loc[0]
    new_df.reset_index(inplace=True)
    new_df = new_df.rename(columns={"index":"Year"})
    return new_df


# In[122]:


# china's pop growth A
china_popg_a = new_df(pop_a,"Population Annual % Growth")
# china's pop growth B
china_popg_b = new_df(pop_b,"Population Annual % Growth")
display(china_popg_a)


# In[123]:


# merge GDP & Population Growth data
# Group A
china_grp_a = pd.merge(china_popg_a,gdp_a)
# fill N/A value in GDP w/ https://en.wikipedia.org/wiki/Historical_GDP_of_China (1960 --> 8.0 % GDP annual growth)
#china_grp_a = china_grp_a.fillna(8)
display(china_grp_a)


# In[124]:


# Group B
china_grp_b = pd.merge(china_popg_b,gdp_b)
display(china_grp_b)


# In[125]:


# add china's female population data (% of total population), for gender equity analysis (found evidence to suggest on child policy caused a gender imbalance with more male than females due to cultural beliefs & practices)
fpop_data = pd.read_csv("API_SP.POP.TOTL.FE.ZS_DS2_en_csv_v2_9945099.csv",skiprows=3)
display(fpop_data)


# In[126]:


china_fpop_data = fpop_data[fpop_data["Country Name"]=="China"]
display(china_fpop_data)


# In[127]:


fpop_a = china_fpop_data.iloc[:,4:23]
fpop_a.index = [0]
fpop_b = china_fpop_data.iloc[:,23:len(china_fpop_data.columns)-2]
fpop_b.index=[0]


# In[128]:


china_fpop_a = new_df(fpop_a,"Female Population (% of total population)")
china_fpop_b = new_df(fpop_b,"Female Population (% of total population)")
china_fpop_a = china_fpop_a.reindex()
display(china_fpop_a)


# In[129]:


#new_fpop_a = pd.DataFrame(columns=["Year","Female Population (% of total population)"])
#new_fpop_a["Year"] = pd.Series([str(i) for i in list(range(1941,1979))])
#new_fpop_a["Female Population (% of total population)"]= china_fpop_a["Female Population (% of total population)"]
#new_fpop_a["Female Population (% of total population)"] = new_fpop_a["Female Population (% of total population)"].shift(19)
#new_fpop_a.fillna(method='bfill',inplace=True)
#fillna((china_gdp.loc[(china_gdp["Year"]<1940)&(china_gdp["Year"]>1928),"Real GDP per capita"].values.mean()),inplace=True)
#display(new_fpop_a)


# In[132]:


china_grp_a = pd.merge(china_grp_a,china_fpop_a)
display(china_grp_a)


# In[131]:


china_grp_b = pd.merge(china_grp_b,china_fpop_b)
display(china_grp_b)


# Sources:
# 1. https://data.worldbank.org/indicator/SP.POP.GROW?end=2016&start=1960&view=chart (Population Growth)
# 2. https://data.worldbank.org/indicator/SP.POP.TOTL.FE.ZS (Female % of total population)
# 3. http://www.populstat.info/Asia/chinac.htm (China population 1941 to 1959)
# 4. https://ourworldindata.org/economic-growth (Average Real GDP per capita, 2011 benchmark)
