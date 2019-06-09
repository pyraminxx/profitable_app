#!/usr/bin/env python
# coding: utf-8

# Profitable App Profiles for the Google Play & Apple Store 
# 
# Aim is finding profitable mobile app profiles
# Apps that are free to download are considered and main source for the revenue is in-app ads which means that revenue is effected by the number of users.We will try to find the apps that attract more users.

# In[4]:


from csv import reader
#importing GOOGLE PLAY dataset
opened_file = open('googleplaystore.csv',encoding="utf8")
read_file = reader(opened_file)
android = list(read_file)
android_header = android[0]
android = android[1:]

#importing APPLE STORE dataset
opened_file_1 = open('AppleStore.csv',encoding="utf8")
read_file_1 = reader(opened_file_1)
ios = list(read_file_1)
ios_header = ios[0]
ios = ios[1:]


# In[5]:


#taking a sample from dataset
def explore_data(dataset,start,end,rows_cols=False):
    sample = dataset[start:end]
    for row in sample:
        print(row)
        print('/n')  #adding extra row 
    if rows_cols:
        print('Number of rows:',len(dataset))
        print('Number of columns:',len(dataset[0]))


# In[6]:


#printing first three rows of GOOGLE PLAY
print(android_header)
print('\n')
explore_data(android,0,3,True)
#printing first three rows of APP STORE
print('\n')
print(ios_header)
print('\n')
explore_data(ios,0,3,True)


# In[7]:


del android[10472] #deleting incorrect data


# In[8]:


#seperating duplicated rows from dataset
duplicate=[]
unique=[]
for app in android:
    name = app[0]
    if name in unique:
         duplicate.append(name)
    else:
        unique.append(name)
        
print('Number of duplicate apps:', len(duplicate))       


# In[9]:


print('Expected length:',len(android)-1181)


# In[10]:


#removing the duplicates that has lower reviews
reviews_max = {}  #creating empty dictionary
for app in android:
    name = app[0]                #app name
    n_reviews = float(app[3])       #number of reviews
    if name in reviews_max and  reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
    elif name not in reviews_max:
        reviews_max[name] = n_reviews    #key is name of the app
android_clean = []      #to store cleaned data 
already_added = []      #to store app names
for app in android:
    name = app[0]
    n_reviews = float(app[3])
    
    if (reviews_max[name] == n_reviews) and (name not in already_added):
        android_clean.append(app)
        already_added.append(name)


# In[11]:


explore_data(android_clean, 0, 3, True)   #controlling


# In[12]:


#removing non-english apps
#characters that have ASCII number less than 127 are belong to English
def english(a_string):
    non_ascii = 0
    for index in a_string:
        if ord(index) > 127:
            non_ascii += 1
    if non_ascii > 3:
        return False
    else:
        return True
        
print(english('Instgram'))
print(english('爱奇艺PPS -《欢乐颂2》电视剧热播'))
print(english('Instachat 😜'))
print(english('Docs To Go™ Free Office Suite'))


# In[13]:


#filtering out non-english from both datasets
android_english=[]
ios_english=[]
for app in android_clean:
    name = app[0]
    if english(name):
        android_english.append(app)
        
for app in ios:
    name = app[1]
    if english(name):
        ios_english.append(app)
        
explore_data(android_english, 0, 3, True)
print('\n')
explore_data(ios_english, 0, 3, True)        


# In[14]:


#filtering out non-free aps
android_final = []
ios_final = []
for app in android_english:
    price = app[7]
    if price == '0':
        android_final.append(app)
        
for app in ios_english:
    price = app[4]
    if price == '0.0':
        ios_final.append(app)
        
print(len(android_final))    #checking
print(len(ios_final))        


# In[15]:


#we are trying to find an app profile that fits both APP STORE and GOOGLE PLAY
#generating frequency table  (finding out common genres)

#function for showing percentages
def freq_table(dataset,index):
    table = {}
    total = 0
    for row in dataset:
        total += 1
        value = row[index]
        if value in table:
            table[value] += 1
        else:
            table[value] = 1
       
    table_percen = {}
    for key in table:
        percentage = (table[key]/total) *100
        table_percen[key] = percentage
    return table_percen

#function for displaying percentages in a descending order
def display_table (dataset,index):
    table = freq_table(dataset,index)
    table_display = []
    for key in table:
        key_value_tuple = (table[key],key)  #transforming to list of tuples(for sorting)
        table_display.append(key_value_tuple)
    
    sorted_table = sorted(table_display,reverse = True)  #reverse parameter controls the order
    for entry in sorted_table:
        print(entry[1],':',entry[0])
        
#frequency table for android
display_table(android_final,1)  #category column

#frequency table for ios
display_table(ios_final,-5)   #prime_genre column


# In[16]:


#to find the most popular app we can calculate average number of installs for each genre
#calculating average number of user ratings on APP STORE
genres_ios = freq_table(ios_final,-5)    #prime_genre column
for genre in genres_ios:
    total = 0     #sum of user ratings 
    len_genre = 0  #number of apps 
    for app in ios_final:
        genre_app = app[-5]    
        if genre_app == genre:
            n_ratings = float(app[5])   #rating_count_tot column
            total += n_ratings
            len_genre += 1
            
    avg_ratings = total/len_genre
    print(genre,':',avg_ratings)


# In[19]:


categories_android = freq_table(android_final, 1) #category column
for category in categories_android:
    total = 0         #to store sum of installs
    len_category = 0
    for app in android_final:
        category_app = app[1]    #app genre
        if category_app == category:
            n_installs = app[5]
            #removing any  + or , character
            n_installs = n_installs.replace(',', '')
            n_installs = n_installs.replace('+', '')
            total = float(n_installs)
            len_category += 1
            
    avg_installs = total / len_category
    print(category,':',avg_installs)
        






