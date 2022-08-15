#!/usr/bin/env python
# coding: utf-8

# # case study 2.3
# ### Analysis of the hourly details of the users
# * we have three hourly details of the users, hourly calories, hourly intensities, hourly steps

# In[3]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[4]:


df=pd.read_csv("/home/sunit.kapuria/data analyst course/case_study_2/Fitabase Data 4.12.16-5.12.16/hourlyCalories_merged.csv")


# In[5]:


df1=pd.read_csv("/home/sunit.kapuria/data analyst course/case_study_2/Fitabase Data 4.12.16-5.12.16/hourlyIntensities_merged.csv")


# In[112]:


df2=pd.read_csv("/home/sunit.kapuria/data analyst course/case_study_2/Fitabase Data 4.12.16-5.12.16/hourlySteps_merged.csv")


# In[138]:


df.head(24)


# In[16]:





# In[8]:


df.info()


# In[9]:


df1.head(2)


# In[10]:


df2.head(3)


# In[11]:


df['ActivityHour']=pd.to_datetime(df['ActivityHour'])
df1['ActivityHour']=pd.to_datetime(df1['ActivityHour'])
df2['ActivityHour']=pd.to_datetime(df2['ActivityHour'])


# In[ ]:


# df.info()
# df1.info()
# df2.info()


# In[ ]:


# df['Id'].count()
# df1['Id'].count()
# df2['Id'].count()
# All of them contains equal number of data


# In[ ]:


# x=df['Id']-df1['Id']
# x.sum()
# x=df1['Id']-df2['Id']
# x.sum()


# Since the Ids are number format, we can check the difference between the Ids of each dataframe to check if they are aligned to each other.
# * from above experiment we can see that the Ids of each dataframes are alinged to each other

# ### lets merge the three dataframes column wise, so that we can have all the data in a single data frame

# In[21]:


inner_join = pd.merge(df.drop('ActivityHour', axis=1),
                      df1.drop('ActivityHour', axis=1), 
                      on ='Id',
                      how='inner')


# In[22]:


inner_join.head()


# * as we can see here pd.merge is giving wrong values for calories, and the reason for this is there are repeated values of 
# Id for each user. Therefore we will have to merge the data by simply concatenating. 
# * another way we can apply is by first performing the aggregation and then merging using pd.merge
# *Lets go with the send method

# ### Lets perform the aggregration and find out hourly calories burned for each user

# In[24]:


df.head()


# In[25]:


df.info()


# In[28]:


df_count=df.groupby('Id').count()['ActivityHour']


# In[36]:


df_count
#The average count of each user is more or less same
df_count.mean()


# In[32]:


df_new=df.groupby('Id').sum()['Calories']


# In[33]:


calories_hr=df_new/df_count


# In[116]:


calories=pd.Series(calories_hr, name='calories')
calories=calories.to_frame()


# In[105]:


type(calories)


# In[106]:


calories.reset_index(inplace=True)


# In[107]:


calories.head()


# * This is the average hourly calories burned each user

# ### Lets perform the aggregration and find out hourly intensity of each user

# In[37]:


df1.head()


# * We are not droping the zero values in the intensities as it shows that the user was tracking his/her intensities during the
# ideal periods as well, so we will include those values to calculate the average

# In[38]:


df1.info()


# * in this df1, sum the total intensity and divide it with the total number of hours per users. 
# * lets do both and cross check

# In[52]:


df1_count=df1.groupby('Id').count()['ActivityHour']
df1_new=df1.groupby('Id').sum()['TotalIntensity']
intensities_hr=df1_new/df1_count
intensities_hr


# In[53]:


df1_new1=df1.groupby('Id').sum()['AverageIntensity']
avg_intensities_hr=df1_new1/df1_count
avg_intensities_hr


# In[70]:


new_df1=pd.concat([intensities_hr,avg_intensities_hr], axis=1)


# In[72]:


new_df1.reset_index(inplace=True)


# In[78]:


new_df1.rename(columns={'0':'Total_intensity_hr', '1':'avg_intensity_hr'}, inplace=True)


# In[83]:


new_df1.columns=['Id','Total_intensity_hr', 'avg_intensity_hr']


# In[99]:


new_df1.head()


# In[100]:


# new_df1.to_csv('/home/sunit.kapuria/data analyst course/case_study_2/details_hr')


# ### Lets join the agregrated information form the average intensity and average calories infomation

# In[108]:


inner_join = pd.merge(new_df1,
                      calories, 
                      on ='Id',
                      how='inner')


# In[110]:


inner_join.columns=['Id','Total_intensity_hr', 'avg_intensity_hr', 'Calories_hr']


# In[111]:


inner_join.head()


# ### Lets perform the same process for hourly steps caculation

# In[113]:


df2.head()


# In[114]:


df2.info()


# In[117]:


df2['ActivityHour']=pd.to_datetime(df2['ActivityHour'])


# In[118]:


df2_count=df2.groupby('Id').count()['ActivityHour']


# In[119]:


df22_new=df2.groupby('Id').sum()['StepTotal']


# In[120]:


steps_hr=df22_new/df2_count


# In[121]:


steps_hr=pd.Series(steps_hr, name='steps_hr')
steps_hr=steps_hr.to_frame()


# In[122]:


steps_hr.reset_index(inplace=True)


# In[123]:


steps_hr.head()


# Lets merge it with the previous newly merged dataframe

# In[124]:


final_join = pd.merge(inner_join,
                      steps_hr, 
                      on ='Id',
                      how='inner')


# In[125]:


final_join.head()


# * Lets now check the visualize the relation between each of the features

# In[126]:


sns.pairplot(final_join.iloc[:,1:])


# #### It is quite visible that average intensity and total intensity are completely correlated to each other so we will drop average intensity here. 
# * Lets find the correlation value between intenisty and calorie burned and also steps per hr

# In[127]:


final_join.drop('avg_intensity_hr', axis=1, inplace=True)


# In[128]:


sns.pairplot(final_join.iloc[:,1:])


# In[129]:


import statistics
from scipy.stats import pearsonr


# In[130]:


list1 = final_join['Total_intensity_hr']
list2 = final_join['Calories_hr']

# Calculating pearson correlation
corr, _ = pearsonr(list1, list2)
print('%.3f' % corr)
print('\n\n')


# In[131]:


list1 = final_join['Total_intensity_hr']
list2 = final_join['steps_hr']

# Calculating pearson correlation
corr, _ = pearsonr(list1, list2)
print('%.3f' % corr)
print('\n\n')


# In[132]:


list1 = final_join['Calories_hr']
list2 = final_join['steps_hr']

# Calculating pearson correlation
corr, _ = pearsonr(list1, list2)
print('%.3f' % corr)
print('\n\n')


# 

# * this shows that while all three of these variables are positively correlated, there is maximum correlation between Total intensity and total steps per hour, while calories per hour is only 44% correlated to both of them.

# Let us save the new dataframe as hourly_info

# In[134]:


final_join.to_csv('/home/sunit.kapuria/data analyst course/case_study_2/hourly_info.csv')


# ## we can further check the slope of fitted line between any of these two variables

# In[ ]:




