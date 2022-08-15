#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# Lets check at which time of the day a person users are most active
# * we will divide the 24 hours into 6 categories: '12am-3am', '4am-7am', '8am-11am', '12pm-3pm', '4pm-7pm', '8pm-11pm'

# In[2]:


df=pd.read_csv("/home/sunit.kapuria/data analyst course/case_study_2/Fitabase Data 4.12.16-5.12.16/hourlyCalories_merged.csv")


# In[3]:


df['ActivityHour']=pd.to_datetime(df['ActivityHour'])


# In[4]:


df.info()


# In[5]:


df.head(5)


# In[8]:


df['date']=df['ActivityHour'].dt.date


# In[9]:


df.head(2)


# In[10]:


df['hour']=df['ActivityHour'].dt.hour


# In[11]:


df.head(2)


# In[36]:


def hourly(x):
    if x in [0,1,2,3]:
        return 1
    elif x in [4, 5,6,7]:
        return 2
    elif x in [8,9,10,11]:
        return 3
    elif x in [12,13,14,15]:
        return 4
    elif x in [16,17,18,19]:
        return 5
    else:
        return 6
    


# In[37]:


df['hour_cat']=df['hour'].apply(hourly)


# In[38]:


df.head()


# In[39]:


xx=df.groupby('hour_cat').mean()[['Calories']]


# In[41]:


fig, ax = plt.subplots()
plt.plot(xx)
plt.xlabel('Category')
ax.set_xticks((1,2,3,4,5,6))
ax.set_xticklabels(('12am-3am', '4am-7am', '8am-11am', '12pm-3pm', '4pm-7pm', '8pm-11pm'))


# This shows that maximum activity is recorded between 8 am to 7pm, with maximum between 4 Pm to 7pm

# ### Users are most active between 8 am to 7pm. with maximum activity betwen 4 pm to 7pm.
# #### Least activity is in the sleeping hours of 12 am-3am, with gradual increase in the activity

# ### Lets now check the activity by each hour

# In[43]:


yy=df.groupby('hour').mean()['Calories']


# In[56]:


fig, ax = plt.subplots()
plt.plot(yy)
plt.xlabel('24 hours')
ax.set_xticks(yy.index)


# In[ ]:





# In[52]:


yy.sort_values(ascending=False).plot()


# In[59]:


yy[yy>100]


# ## This shows that the most active hours of users are between 8 am to 8pm where the average calories burn as above 100 per hour

# In[ ]:




