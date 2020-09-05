import pandas as pd 
import numpy as np
import warnings
#import seaborn as sns
import matplotlib.pyplot as plt
#%matplotlib inline
warnings.filterwarnings('ignore')


def Recommend_Movies(s):
    # Let’s assume that a user has watched movie(s)
    # The goal is to look for movies that are similar to Contact (1997) and Air Force One (1997 which we shall recommend to this user. 
    s_user_rating = movie_matrix[s]
    #print(s_user_rating.head(50))

    similar_to_s =movie_matrix.corrwith(s_user_rating)
    #print(similar_to_s.head(50))

    corr_s = pd.DataFrame(similar_to_s, columns=['Correlation'])
    corr_s.dropna(inplace=True)
    #print(corr_s.head())

    corr_s = corr_s.join(ratings['number_of_ratings'])
    #print(corr_s .head())

    mo = corr_s[corr_s['number_of_ratings'] > 100].sort_values(by='Correlation', ascending=False).head(10)

    return mo

df = pd.read_csv('ratings.csv')

#print(df.head(5))

movie_titles = pd.read_csv('movies.csv')
#print(movie_titles.head())

df = pd.merge(df, movie_titles, on='item_id')
#print(df.head())
#print(df.describe())

ratings = pd.DataFrame(df.groupby('title')['rating'].mean())
#print(ratings.head())

ratings['number_of_ratings'] = df.groupby('title')['rating'].count()
#print(ratings.head(20))

#import matplotlib.pyplot as plt
#%matplotlib inline
ratings['rating'].hist(bins=50)
#plt.show()
ratings['number_of_ratings'].hist(bins=10)
#plt.show()

#  now check the relationship between the rating of a movie and the number of ratings. We do this by plotting a scatter plot using seaborn.
import seaborn as sns; sns.set(style="darkgrid")
sns.jointplot(x='rating', y='number_of_ratings', data=ratings)
#plt.show()
#  The graph indicates that the more the ratings a movie gets the higher the average rating it gets. 
#  This is important to note especially when choosing the threshold for the number of ratings per movie.

movie_matrix = df.pivot_table(index='user_id', columns='title', values='rating')
#print(movie_matrix.head(50))

ratings.sort_values('number_of_ratings', ascending=False).head(10)


a = 'Air Force One (1997)'
b = 'Contact (1997)'

#rmovies = Recommend_Movies(a)
#print('Movies You may Like...............')
#print(rmovies)

#for i in rmovies.index:
#    print(rmovies['Correlation'][i], i)