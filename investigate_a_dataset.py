# -*- coding: utf-8 -*-
"""2Investigate_a_Dataset.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tFYxJQGw-RBaWXcZcro-ztR-SrO9InUC

# Project: Investigate `TMDB Movie DataSet`

---

## Table of Contents
<ul>
<li><a href="#Introduction">Introduction</a></li>
<li><a href="#wrangling">Data Wrangling</a></li>
<li><a href="#eda">Exploratory Data Analysis</a></li>
<li><a href="#conclusions">Conclusions</a></li>
</ul>

<a id='Introduction'></a>

## Introduction About DataSet

<blockquote>
<h3> For Data Analysis I have Choosen TMDB Movie Dataset </h3>
<h4> About TMDB Movie Dataset </h4>
It store the movies data more then 10,000 from the year 1960 to 2015 
</blockquote>

## Process

<blockquote>

### Question's I'm Going To Work
- 1) Highest Profitable movie all over the year of 1960 to 2015 
    <br> (Low Budget High Revenue)
   
- 2) Most used keywords all over the year of 1960 to 2015 <br>
(Done by Extracting a Keyword String)

- 3) Movie production just exploded in year between 1980 to 1990.
<br> It could be due to advancement in technology and commercialisation of internet.

- 4) Number of Movies Directed by the `Director` from 1960 to 2015

- 5) Movies Genre which are very much liked by the audience

</blockquote>


---
<blockquote>

### Importing Libraries 
</blockquote>

---

<blockquote>

### Data Wrangling 
- 1) Gathering of data
- 2) Assessing of data
- 3) Data Cleaning
</blockquote>

---
<blockquote>

### EXPLORATORY DATA ANALYSIS (EDA) 
- 1) Analyzing
- 2) Visualizing
- 3) Feature Engineering
</blockquote>

---
<blockquote>

### CONCLUSION 
</blockquote>

---

### **Importing Libraries**

I used Plotly for multiple plot to install this lib follow the below command <br>
pip install plotly==4.7.1 <br>
But for now i'm using seaborn and matplotlib
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import plotly.express as px
import seaborn as sns

"""<a id='wrangling'></a>
## Data Wrangling

<!-- > **Tip**: In this section of the report, you will load in the data, check for cleanliness, and then trim and clean your dataset for analysis. Make sure that you document your steps carefully and justify your cleaning decisions. -->

Loading the Dataset
"""

df = pd.read_csv("tmdb-movies.csv")
# Going to backup this dataset for future purpose 
df_cpy = df.copy()

"""Going to Remove the columns which doesn't possess any useful information"""

df.drop(['id','imdb_id','homepage','tagline','overview','production_companies','budget_adj','revenue_adj','keywords'], axis = 1 , inplace=True)

"""Renaming some columns with easy to understand and meaningful"""

df.rename(columns={'original_title': 'movie','vote_count': 'vote','vote_average': 'rating','release_year': 'year'},inplace=True)

"""Assessing of data"""

print("Rows : ",df.shape[0])
print("Columns : ",df.shape[1])

df.info()

df.describe()

print("Count of Nan Columns")
df.isna().sum()

"""### Data Cleaning

Filling the Nan value <br>
"""

# By analysis we found that the most nan value found in cast was related to generes
df[df["cast"].isnull()].genres.unique()

# If we see the above List we can easly say that In genres (Documentary, Animation , and Drama) is holding Max nan value in 
df[df['cast'].isna()].head(5)

# If we just cross check by using those Geners we found the below result
i=0
temp = df[df['cast'].isna()]
for index, row in temp.iterrows(): 
    if(type(row["genres"]) == str):
        if('Documentary' in row["genres"].split('|') or 'Animation' in row["genres"].split('|') or 'Drama' in row["genres"].split('|')) :
            i=i+1
print("Overall 74 Nan Value was hold by this three Geners Category (Documentary, Animation , and Drama)" , i)

# Total 76 Nan Value in genres
#  And this three Geners Category (Documentary, Animation , and Drama) possess 74 Nan Value

# So I'm going to fill the Geners with No_cast value
df['cast'].fillna('No_Cast' , inplace=True)

print("Count of Nan Columns")
df.isna().sum()

"""Droping Duplicate rows"""

print('Before Dropping ' , df.duplicated().sum())
df.drop_duplicates(inplace=True)
print('After Dropping ' , df.duplicated().sum())

"""Droppping Rows with Nan Values"""

df[df['director'].isna()].head(5)

# If we Notice the below rows does not possess most values so we are going to drop that rows
df[df["genres"].isnull() & df["director"].isnull()]

# Going to drop above rows
gen_dir = df[df["genres"].isnull() & df["director"].isnull()].index
df.drop(gen_dir,inplace=True)

# As the Genres which hold Nan value dont possess budget , revenue & genres
df[df['genres'].isna()].head(5)

# Because Lack of information in the above rows i'm going to remove it
gen = df[df["genres"].isnull()].index
df.drop(gen,inplace=True)

# Where director rows are nan parallel revenu and budget is also zero   
df[df['director'].isna()].head(5)

# so i'm going to drop it
dire = df[df["director"].isnull()].index
df.drop(dire,inplace=True)

df.isna().sum()

# Before we removing Nan rows the Total Rows are 10865
# After removing it become 10799



"""Variable Conversion"""

df.info()

# Based on the info there is only one column 'release_date' is possess different datatype
df["release_date"]= pd.to_datetime(df["release_date"])



"""<a id='eda'></a>
## Exploratory Data Analysis


### Feature Engineering
"""

def profit_cal():
    # We Create new Column saying Gross Profit 
    # If we just subtract revenue & budget we end up with wrong conclusion 

    # (Total Revenue / Total Expense )*100
    # 8169363/8175346*100

    df['g_profit'] = round((df['revenue']/df['budget'])*100)

    # if we encounter any misplaced value such as zero revenue or zero budget we end up with na value so we explicitly fill na with zero
    df['g_profit'].replace([np.inf, -np.inf], np.nan , inplace=True)
    df['g_profit'].fillna(0,inplace=True)
profit_cal()

df.head(1)



"""### Research Question 1 

> Highest Profitable movie all over the year of 1960 to 2015 <br>
(Low Budget High Revenue)
"""

df.sort_values(['g_profit'], ascending = False).head(5)

# If we notice the budget of some movies got wrong so we need to fill it manually  
df.loc[10495,'budget'] = 13000000
df.loc[6179,'budget'] = 7500000
df.loc[3608,'budget'] = 3000000
profit_cal()

# After completing this manual process we call 'profit_cal()'
# its become a long process to find and all outlier values manually so i stopped it 
# Solution for this process is webscripping were we can find the value from sources and we can fill it

df.sort_values(['g_profit'], ascending = False).head(5)



"""### Research Question 2

> Most used keywords all over the year of 1960 to 2015 <br>
(Done by Extracting a Keyword String)
"""

# Steps
# First Run a Loop using the count of keyword
# Second run inner loop to split a string for each keyword and add into a list
# Third when Outer loop complete create a dictionary with unique value from list and add the count beside it 
# So we get two information from it One Unique Keywords and the repetaion of keywords used in this dataset

df_cpy.keywords

key_store = []
for key in df_cpy.keywords:
    if(type(key) == str):
        for individual_key in key.split('|'):
            key_store.append(individual_key)

# Total Keywords
len(key_store)

# Unique Keywords
x = np.array(key_store) 
len(np.unique(x))

# Creating a Dictionary with keyword and count (how many times it used)
freq = {} 
for items in key_store: 
    freq[items] = key_store.count(items)

# displaying just first 5 out of 7878 dictionary
from itertools import islice
def take(n, iterable):
    return list(islice(iterable, n))

n_items = take(5, freq.items())
n_items

sort_keywords_based_on_count = sorted(freq.items(), key=lambda x: x[1],reverse=True)

key = []
value=[]
for arr in sort_keywords_based_on_count:
    if(arr[1] > 99):
        key.append(arr[0])
        value.append(arr[1])

list_of_tuples = list(zip(key, value))  
keyword_df = pd.DataFrame(list_of_tuples, columns = ['Keyword', 'Keywords_Repeted'])  
keyword_df

"""### Whcih Keyword has Used Most throught out the years is described using **Bar Plot Visualization**"""

# plotly graph
# fig = px.bar(keyword_df, x='Keyword', y='Keywords_Repeted',
#              hover_data=['Keyword', 'Keywords_Repeted'], color='Keywords_Repeted',
#              labels={'pop':'population of Canada'}, height=400)
# fig.show()

f, (ax1) = plt.subplots(figsize=(30, 7), sharex=True)
sns.barplot(x=keyword_df.Keyword, y=keyword_df.Keywords_Repeted, ax=ax1)
ax1.axhline(0, color="k", clip_on=True)
plt.ylabel('Keywords_Repeted', fontsize=16)
ax.set_xlabel('Keyword',fontsize=26)
sns.despine(bottom=True)

"""### Research Question 3
Histogram of Movie Released
> Movie production just exploded in year between 1980 to 1990.
<br> It could be due to advancement in technology and commercialisation of internet.

### To Showcase the frequency of movies released in **DistantPlot Visualization**
"""

a4_dims = (28, 8)
sns.set_color_codes()
f, (ax1) = plt.subplots(figsize=(30, 7), sharex=True)

sns.distplot(df.year,color="y", kde=False, rug=True);

plt.ylabel('Movies_Released Count', fontsize=16)
ax.set_xlabel('Year',fontsize=16)
sns.despine(bottom=True)

df_cpy.director.head(10)

"""### Research Question 4
Number of Movies Directed by the `Director` from 1960 to 2015
"""

dir_store = []
for key in df_cpy.director:
    if(type(key) == str):
        for individual_key in key.split('|'):
            dir_store.append(individual_key)

# Total Directors with repeation
len(dir_store)

# Unique Directors Count
x = np.array(dir_store) 
len(np.unique(x))

# Creating a Dictionary with Name and count (how many times it used)
dir_freq = {} 
for items in dir_store: 
    dir_freq[items] = dir_store.count(items)

# displaying just first 5 out of 5362 dictionary
from itertools import islice
def take(n, iterable):
    return list(islice(iterable, n))

n_items = take(5, dir_freq.items())
n_items

sort_dir_based_on_count = sorted(dir_freq.items(), key=lambda x: x[1],reverse=True)  
# sort_dir_based_on_count

dir_key = []
dir_value=[]
for arr in sort_dir_based_on_count:
    if(arr[1] > 0):
        dir_key.append(arr[0])
        dir_value.append(arr[1])

list_of_tuples = list(zip(dir_key, dir_value))  
dir_df = pd.DataFrame(list_of_tuples, columns = ['Director_Name', 'Frequency_Directed'])  
highly_directed = dir_df.head(20)

"""### Which Director has Directed Most high number of movies through out the years is described using **Bar Plot Visualization**"""

# plotly graph

# fig1 = px.bar(highly_directed, x='Director_Name', y='Frequency_Directed', 
#               title="Top 20 Director's with high Count of movie Driected",
#               color_discrete_sequence=['indianred'],
#              )
# fig1.show()

sns.set_color_codes()
f, (ax1) = plt.subplots(figsize=(30, 7), sharex=True)
sns.set(style="whitegrid")

ax = sns.barplot(x="Director_Name", y="Frequency_Directed", data=highly_directed)

plt.ylabel('Frequency_Directed', fontsize=16)
ax.set_xlabel('Director_Name',fontsize=16)
sns.despine(bottom=True)

highly_directed

highly_directed.Director_Name.values

from wordcloud import WordCloud
import matplotlib.pyplot as plt
 
# initialize an empty string 
str1 = ""  

# traverse in the string   
for ele in highly_directed.Director_Name.values:  
    str1 += ele   

wordcloud = WordCloud(width=800, height=500, margin=10).generate(str1)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.margins(x=0, y=0)
plt.show()

"""### Research Question 5
Movies Genre which are very much liked by the audience
"""

df.genres.nunique()

# Splitting Geners string in to individual list
 
genres_store = []
for key in df.genres:
    if(type(key) == str):
        for individual_key in key.split('|'):
            genres_store.append(individual_key)

#  From the derived list converting in to unique list
genres_list = list(set(genres_store))

# There are total 20 Geners
genres_list

# As per the frequency im going to use the top 5 geners name and grouping as others column as one
freq_g = {} 
for items in genres_store: 
    freq_g[items] = genres_store.count(items)

freq_g

# Displaying Geners Count in Desending order
geners_in_des = sorted(freq_g.items(), key=lambda x: x[1],reverse=True)    
geners_in_des

# Im going to take the geners as a columns which have more then 1000 count 
genre_key = []
genre_value=[]
for arr in geners_in_des:
    genre_key.append(arr[0])
    genre_value.append(arr[1])

list_of_tuples = list(zip(genre_key, genre_value))  
genre_df = pd.DataFrame(list_of_tuples, columns = ['Genere', 'Most_Watched'])  
genre_df
# highly_directed

"""### Which Genres has Audience liked most is described using **Bar Plot Visualization**"""

# fig = px.bar(   
#         x=genre_df.Most_Watched, 
#         y=genre_df.Genere, 
#         labels={'x':'Viewer Watched Frequency', 'y':'Genre'},
#         orientation='h',
#         height = 700,
#         )
# fig.show()


f, (ax1) = plt.subplots(figsize=(30, 7), sharex=True)
ax = sns.barplot(x='Most_Watched', y='Genere', data=genre_df)
plt.ylabel('Genere Most_Watched', fontsize=16)
ax.set_xlabel('Viewer Watched Frequency',fontsize=16)
sns.despine(bottom=True)

"""### Audience Prefered Genres shown in percentage using pie Chart"""

# fig = px.pie(genre_df, values='Most_Watched', names='Genere')
# fig.update_traces(textposition='inside')
# fig.show()

labels = genre_df.Genere
sizes = genre_df.Most_Watched
explode = np.repeat(0,genre_df.shape[0]-1)
exp = explode.tolist()
exp[0:3] = [0.1,0.1,0.1,0.1]



fig1, ax1 = plt.subplots(figsize=(15, 15))
fig1.subplots_adjust(0.3,0,1,1)

ax1.pie(sizes,explode=exp, labels=labels, autopct='%1.1f%%', shadow=True, startangle=320)
ax1.axis('equal') 

plt.show()

exp

"""Based on above chart we can say that huge amount audiounce are more attracted to Drama, Comedy, Thriller & Action then other Genres

Some General Analysis
"""

corr = df.corr()
mask = np.zeros_like(corr)
mask[np.triu_indices_from(mask)] = True
with sns.axes_style("white"):
    f, ax = plt.subplots(figsize=(7, 5))
    ax = sns.heatmap(corr, mask=mask, vmax=.3, square=True)

"""Removing Outlier from this dataset <br>
By removing Outlier of individual Column `Runtime` is Significantly removed all other column's outlier
"""

q_low = df["runtime"].quantile(.028)
q_hi  = df["runtime"].quantile(0.97)
df_filtered = df[(df["runtime"] < q_hi) & (df["runtime"] > q_low)]

"""General Idea using **Pairplot Visulazation** to find the correlation between each columns"""

sns.pairplot(df_filtered);

df_filtered.rating.describe()

df_filtered.groupby(['year'])['budget'].sum().sort_values(ascending=False).head(10)

df_filtered.groupby(['year'])['revenue'].sum().sort_values(ascending=False).head(10)



"""<a id='conclusions'></a>
## Conclusions

The preparation of the data, the modeling of these data, then the visualization of these data with a variety of graphs, and finally the interpretation of these graphs & numbers made it possible to conduct an analysis on the TMDB Movie Dataset





## **Challenges I Faced in this Dataset:**
- Its little Tricky to split Keywords and genres from Sting to individual list with its Count
- Deciding Which Column is not usefull for my analysis because Maximum Columns inside this dataset are Categorial Variable's
- Most of the Budget and Revenu Columns ae miss filled so it take me to fill some of the data manually 
- Finally Deciding which Question is Sutiable for this dataset is really a best part which i worked hard



---





## **This study through a large volume of data, allowed me to determine the following points for movies between 1966 to 2015:** <br>
Some Of the Prediction off the Question's

- Audience Ratings: Most of the audience ratings are between 5.5/10 and 7/10. <br>
- Based on the Dataset the film industry has spend more on production on 2010 followed by 2013 and 2011 <br>
- Most Revenue Generated Year was 2015 followed by 2013 & 2014 <br>
- Most movies last between 60 minutes and 120 minutes <br>
- Movies Revenue Is Highly Correlated With Popularity <br>
"""



"""### Referred to complete this Project
Kaggle <br>
Github <br>
"""

