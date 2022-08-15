#!/usr/bin/env python
# coding: utf-8

# # Case study 2: 
# #2. Understanding the sleep pattern and other important insights
# 

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[2]:


df=pd.read_csv("/home/sunit.kapuria/data analyst course/case_study_2/Fitabase Data 4.12.16-5.12.16/sleepDay_merged.csv")


# In[3]:


df.head()


# In[4]:


df.info()


# In[33]:


df['Id'].nunique()


# ### we have sleep data for 24 users out of total 34 users. 
# * This shows that some of the users are not comfortable wearing the smartdevice while sleeping
# * The analysis will have to be carried on the 24 users 

# "SleepDay" is in object format, lets change that into DateTime format. Also its a per day data so we can drop the time part of the Datetime values.

# In[5]:


df['SleepDay']=pd.to_datetime(df['SleepDay'])


# In[6]:


df.info()


# In[8]:


df['SleepDay']=df['SleepDay'].apply(lambda x: x.date())


# In[9]:


df.head()


# In[26]:


gb=sns.countplot(x='Id', data=df)


# #### Lets see how many records of sleep are there for each user

# In[27]:


x=pd.Series(df.groupby('Id').count()['SleepDay'])
x.sort_values(ascending=False)


# * This shows that some of the users have actively used the device to track the sleep cycle while many of the users have hardly used it to track the sleep.

# Lets now see how many what is the average minutes of sleep Vs average minutes of time in bed for the uses

# In[38]:


gg=df.groupby("Id").mean()[['TotalMinutesAsleep', 'TotalTimeInBed']]


# In[39]:


gg.head(2)


# In[41]:


fig=plt.figure()
gb=sns.lmplot(x='TotalMinutesAsleep', y='TotalTimeInBed',data=gg, fit_reg=True)
gb.fig.set_figwidth(8)
gb.fig.set_figheight(8)
plt.title('Sleep Vs time in bed')


# ### There is a clear positive correlation between the sleep and time in bed , except few outliers. 
# * lets calculate the positive correlation value

# In[42]:


import statistics
from scipy.stats import pearsonr


# In[43]:


list1=gg['TotalMinutesAsleep']
list2=gg['TotalTimeInBed']
corr, _ = pearsonr(list1, list2)
print('%.3f' % corr)


# ### positive correlation 0.94

# Lets concat the count of sleeps, with the new dataframe "gg"

# In[44]:


new_df=pd.concat([gg,x], axis=1)


# In[52]:


new_df.head(5)


# In[47]:


new_df.reset_index(inplace=True)


# In[51]:


new_df.rename(columns={'SleepDay':"count_sleepday"}, inplace=True)


# Lets save this new agregrated csv file for futher analysis through visualization

# In[53]:


new_df.to_csv("/home/sunit.kapuria/data analyst course/case_study_2/new_sleep.csv", index=False)


# In[ ]:




