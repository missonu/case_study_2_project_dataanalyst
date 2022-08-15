#!/usr/bin/env python
# coding: utf-8

# # CASE STUDY 2, 
# #1. Understanding relation between weight and BMI and some other observations

# In[62]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[9]:


df=pd.read_csv("/home/sunit.kapuria/data analyst course/case_study_2/Fitabase Data 4.12.16-5.12.16/weightLogInfo_merged.csv")


# In[12]:


df.head()


# In[7]:


df.info()


# In[11]:


df['Date']=pd.to_datetime(df['Date'])


# In[15]:


sns.heatmap(df.isna())


# It shows that maximum values of Fat is null, which means, the device is not automatically able to fill it and the user are also not very active in filling it

# lets drop the FAT field

# All other field are obserevd to be in right format and there is no missing values

# In[19]:


df.drop(labels=['Fat'], axis=1, inplace=True)


# In[20]:


df.head()


# Lets groupby by ID and check the weights in pounds. We can also drop weight in Kg as the column is repeating.

# In[21]:


df.drop(labels=['WeightKg'], axis=1, inplace=True)


# In[22]:


df.head(2)


# we should round the values in "WeightPounds" upto two decimal point

# In[23]:


df['WeightPounds']=df['WeightPounds'].apply(lambda x: round(x,2))


# In[24]:


df.head(2)


# The "LogId" field does not seem to give any unique information and therefore can be dropped

# In[25]:


df.drop(labels=['LogId'], axis=1, inplace=True)


# In[26]:


df.head(2)


# Let us check what is the average weight and BMI of each user

# In[38]:


g=df.groupby("Id")
g.agg(["count","mean"])[["WeightPounds", "BMI"]]
    


# Few observations:
# * maximum users do not tend to keep track of the weight, BMI, in the tracker.
# * Out of 30 users, we have data only for 8 users here, which indicates that the rest of the user either skipped the process of filling the form, or do not feel the need to use this feature in the smart device.
# * Another reason of having low data for this might be diffulty in filling the values in the device for some reasons.

# Lets check how many of this data is filled manually and how many is filled automatically.

# In[41]:


sns.countplot(x='IsManualReport', data=df)


# This observation shows that most of the values are formed manually by the user. This can be one of the reason behind low data as most users finds it defficult many times to calculate BMI and fill that it. 
# * It might be easier to keep track of the BMI if it is calculated automatically, given that the user only have to fill the weight values.

# In[43]:


g=df.groupby("Id").mean()[["WeightPounds", "BMI"]]
g


# In[48]:


g.reset_index(inplace=True)


# In[49]:


g.head(2)


# Lets check the relation between the two parameters using linear regression

# In[50]:


gb=sns.lmplot(x='WeightPounds', y='BMI', hue='Id',data=g, fit_reg=True)
gb.fig.set_figwidth(8)
gb.fig.set_figheight(8)


# In[52]:


fig=plt.figure()
gb=sns.lmplot(x='WeightPounds', y='BMI',data=g, fit_reg=True)
gb.fig.set_figwidth(8)
gb.fig.set_figheight(8)
plt.title('Weight Vs BMI')


# In[ ]:





# Lets save the average mean, and BMI of these users to a new CSV file for further analysis

# In[59]:


g.to_csv('/home/sunit.kapuria/data analyst course/case_study_2/weightvsbmi.csv', index=False)


# In[60]:


df1=pd.read_csv("/home/sunit.kapuria/data analyst course/case_study_2/weightvsbmi.csv")


# In[61]:


df1.head()


# In[ ]:




