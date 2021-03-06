# -*- coding: utf-8 -*-
"""25_5_22.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1m-hfOx47Xutpjn5WYEMQbE8RG6BE4vH4
"""

#importing libraries
import nltk
nltk.download('punkt')
import nltk
nltk.download('stopwords')
import pandas as pd
import numpy as np
import re
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
from textblob import TextBlob
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
# from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay

#reading data from csv
df = pd.read_csv('SentimentMonitoringDataset.csv', encoding='latin-1')

#analyzing data 
df.head()

df.info()

df.isnull().sum()

df.columns

df.info()

def data_processing(text):
    text = text.lower()
    text = re.sub(r"https\S+|www\S+https\S+", '',text, flags=re.MULTILINE)
    text = re.sub(r'\@w+|\#','',text)
    text = re.sub(r'[^\w\s]','',text)
    text_tokens = word_tokenize(text)
    filtered_text = [w for w in text_tokens if not w in stop_words]
    return " ".join(filtered_text)

df.text = df['text'].apply(data_processing)

text_df = df.drop_duplicates('text')
text_df

stemmer = PorterStemmer()
def stemming(data):
    text = [stemmer.stem(word) for word in data]
    return data

text_df['text'] = text_df['text'].apply(lambda x: stemming(x))

text_df.head()

print(text_df['text'].iloc[0],"\n")
print(text_df['text'].iloc[1],"\n")
print(text_df['text'].iloc[2],"\n")
print(text_df['text'].iloc[3],"\n")
print(text_df['text'].iloc[4],"\n")

text_df.info()

def polarity(text):
    return TextBlob(text).sentiment.polarity

text_df['polarity'] = text_df['text'].apply(polarity)

text_df.head(10)

def sentiment(label):
    if label <0:
        return "Negative"
    elif label ==0:
        return "Neutral"
    elif label>0:
        return "Positive"

text_df['sentiment'] = text_df['polarity'].apply(sentiment)

text_df.head()

fig = plt.figure(figsize=(5,5))
sns.countplot(x='sentiment', data = text_df)

fig = plt.figure(figsize=(7,7))
colors = ("yellowgreen", "gold", "red")
wp = {'linewidth':2, 'edgecolor':"black"}
tags = text_df['sentiment'].value_counts()
explode = (0.1,0.1,0.1)
tags.plot(kind='pie', autopct='%1.1f%%', shadow=True, colors = colors,
         startangle=90, wedgeprops = wp, explode = explode, label='')
plt.title('Distribution of sentiments')

pos_tweets = text_df[text_df.sentiment == 'Positive']
pos_tweets = pos_tweets.sort_values(['polarity'], ascending= False)
pos_tweets.head()

text = ' '.join([word for word in pos_tweets['text']])
plt.figure(figsize=(20,15), facecolor='None')
# wordcloud = WordCloud(max_words=500, width=1600, height=800).generate(text)
# plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title('Most frequent words in positive tweets', fontsize=19)
plt.show()

neg_tweets = text_df[text_df.sentiment == 'Negative']
neg_tweets = neg_tweets.sort_values(['polarity'], ascending= False)
neg_tweets.head()

text = ' '.join([word for word in neg_tweets['text']])
plt.figure(figsize=(20,15), facecolor='None')
# wordcloud = WordCloud(max_words=500, width=1600, height=800).generate(text)
# plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title('Most frequent words in negative tweets', fontsize=19)
plt.show()

vect = CountVectorizer(ngram_range=(1,2)).fit(text_df['text'])

feature_names = vect.get_feature_names()
print("Number of features: {}\n".format(len(feature_names)))
print("First 20 features:\n {}".format(feature_names[:20]))

X = text_df['text']
Y = text_df['sentiment']
X = vect.transform(X)

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

print("Size of x_train:", (x_train.shape))
print("Size of y_train:", (y_train.shape))
print("Size of x_test:", (x_test.shape))
print("Size of y_test:", (y_test.shape))

from sklearn.naive_bayes import MultinomialNB

model = MultinomialNB()
model.fit(x_train, y_train)
classi_pred = model.predict(x_test)
classi_acc = accuracy_score(classi_pred, y_test)
print("Test accuracy sklearn.naive_bayes: {:.2f}%".format(classi_acc*100))

print(confusion_matrix(y_test, classi_pred))
print("\n")
print(classification_report(y_test, classi_pred))

from sklearn.neighbors import KNeighborsClassifier
classi=KNeighborsClassifier(n_neighbors=5,metric='minkowski',p=2)
classi.fit(x_train,y_train)
classi_pred = classi.predict(x_test)
classi_acc = accuracy_score(classi_pred, y_test)
print("Test accuracy KNeighborsClassifier: {:.2f}%".format(classi_acc*100))

print(confusion_matrix(y_test, classi_pred))
print("\n")
print(classification_report(y_test, classi_pred))

style.use('classic')
cm = confusion_matrix(y_test, classi_pred, labels=classi.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix = cm, display_labels=classi.classes_)
disp.plot()

from sklearn.tree import DecisionTreeClassifier
classi_DTC=DecisionTreeClassifier(random_state=0)
classi_DTC.fit(x_train,y_train)
classi_pred = classi.predict(x_test)
classi_acc = accuracy_score(classi_pred, y_test)
print("Test accuracy of DecisionTreeClassifier : {:.2f}%".format(classi_acc*100))

print(confusion_matrix(y_test, classi_pred))
print("\n")
print(classification_report(y_test, classi_pred))

from sklearn.ensemble import RandomForestClassifier
rfclassi=RandomForestClassifier(n_estimators=350,random_state=42)
rfclassi.fit(x_train,y_train)
classi_pred = rfclassi.predict(x_test)
classi_acc = accuracy_score(classi_pred, y_test)
print("Test accuracy of RandomForestClassifier: {:.2f}%".format(classi_acc*100))

print(confusion_matrix(y_test, classi_pred))
print("\n")
print(classification_report(y_test, classi_pred))

import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import GridSearchCV

param_grid={'C':[0.001, 0.01, 0.1, 1, 10]}
# grid = GridSearchCV(LogisticRegression(), param_grid)
# grid.fit(x_train, y_train)

# print("Best parameters:", grid.best_params_)

# y_pred = grid.predict(x_test)

# logreg_acc = accuracy_score(y_pred, y_test)
# print("Test accuracy: {:.2f}%".format(logreg_acc*100))

# print(confusion_matrix(y_test, y_pred))
# print("\n")
# print(classification_report(y_test, y_pred))

from sklearn.svm import LinearSVC

SVCmodel = LinearSVC()
SVCmodel.fit(x_train, y_train)

svc_pred = SVCmodel.predict(x_test)
svc_acc = accuracy_score(svc_pred, y_test)
print("test accuracy of SVCmodel: {:.2f}%".format(svc_acc*100))

print(confusion_matrix(y_test, svc_pred))
print("\n")
print(classification_report(y_test, svc_pred))

grid = {
    'C':[0.01, 0.1, 1, 10],
    'kernel':["linear","poly","rbf","sigmoid"],
    'degree':[1,3,5,7],
    'gamma':[0.01,1]
}
grid = GridSearchCV(SVCmodel, param_grid)
grid.fit(x_train, y_train)

print("Best parameter:", grid.best_params_)

y_pred = grid.predict(x_test)

logreg_acc = accuracy_score(y_pred, y_test)
print("Test accuracy: {:.2f}%".format(logreg_acc*100))

print(confusion_matrix(y_test, y_pred))
print("\n")
print(classification_report(y_test, y_pred))

# saving scikitlearn model
import joblib
#decision tree
joblib.dump(classi_DTC,"dt_model_sentimentAnalysis.pkl")
#naive bayes
joblib.dump(model,"nb_model_sentimentAnalysis.pkl")
# kNeighborsClassifier
joblib.dump(classi,"kn_model_sentimentAnalysis.pkl")
#random forest
joblib.dump(rfclassi,"rf_model_sentimentAnalysis.pkl")
#SVC
joblib.dump(SVCmodel,"svc_model_sentimentAnalysis.pkl")

import joblib
modelss=joblib.load("rf_model_sentimentAnalysis.pkl")

import tweepy

plt.style.use('fivethirtyeight')

consumerKey =  "VH31ywzFkbIVOW7TBckgyc2A0"   
consumerSecret = "PNplfYvlytUz1Cm9LZfwGJhpqajbLuuuDNDjvVGOnDzIYlKXQG"
accessToken =   "1454120698255839236-KCrS90dOiwA9ocQQwUcGaGuV2rWCnO"
accessTokenSecret = "nvX9ZS9fa2vk5SjuoFLUohlro6tKI4BeqNevpsgXjspAs"


#CREATe the authentication object
authenticate=tweepy.OAuthHandler(consumerKey, consumerSecret)

#set the access token and access token secret
authenticate.set_access_token(accessToken,accessTokenSecret)

#create the API object while passing in the auth information
api = tweepy.API(authenticate,wait_on_rate_limit=True)


posts = api.user_timeline(screen_name='@depressingmsgs',count=100,lang='en',tweet_mode='extended')
# posts = api.user_timeline(screen_name='@_SmileGenerator',count=100,lang='en',tweet_mode='extended')
# posts = api.user_timeline(screen_name='@elonmusk',count=100,lang='en',tweet_mode='extended')

count1=0
count2=0
count3=0

i=1

print("Recent tweets by the person are")

for tweet in posts[0:50]:
    # print(str(i)+')'+tweet.full_text + '\n')
    inputtweet=str(i)+')'+tweet.full_text
    print(inputtweet)
    i=i+1 
    review_vector = vect.transform([inputtweet]) # vectorizing
    print(modelss.predict(review_vector))
    if modelss.predict(review_vector)=='Neutral':
        count1=count1+1
    elif modelss.predict(review_vector)=="Positive":
        count2=count2+1
    else:
        count3=count3+1

print("\n")

print("The recent tweets of the person contain :")

print(count1,"neutral tweets") 
print(count2,"positive tweets")
print(count3,"negative tweets")