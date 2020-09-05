from flask import Flask, render_template, url_for, request, redirect
import pandas as pd
import sqlite3  
from movie_recommendation import *

app = Flask(__name__)       # Creating Flask class object

class MyData:
    rows = [0,0,0]
    mids = 'hello aru'
    all_movie = ""          # Stores All movies in  ' movies.csv ' 
    movie_rating = ""       # Stores All movies in  ' ratings.csv '
    recommend = ""
    def fun(self,s):        # Recommended Movies for s from " movie_recommendation.py "
        self.recommend = Recommend_Movies(s)
    def load_all_movies(self):    
        self.all_movie = pd.read_csv('movies.csv')  
    def load_movie_ratings(self):
        self.movie_rating = pd.read_csv('ratings.csv')
    def add_itemid_and_rating_coloumn(self): # Add rating coloum to our 'all_movies' from 'movie_rating'
        li_item_id = []
        li_genre = []
        li_rating = []
        for i in self.recommend.index:
            m_id_1 = -1
            genre_i = ""
            user_i = 0
            rating_i = 0 
            for j in self.all_movie.index:  
                if i==self.all_movie['title'][j] :      # 'i'=movie name in recommender
                    m_id_1 = self.all_movie['item_id'][j]
                    genre_i = self.all_movie['genres'][j]
                    break
                
            for j in self.movie_rating.index:
                if m_id_1== self.movie_rating['item_id'][j] :
                    user_i += 1
                    rating_i += self.movie_rating['rating'][j]
            
            x = rating_i/user_i
            li_item_id.append(m_id_1)
            li_genre.append(genre_i)
            li_rating.append("{:.2f}".format(x))  # formatting upto 2 decimal places

        self.recommend['item_id'] = li_item_id  # add " item " column to recommend
        self.recommend['genre'] = li_genre      # add " genre " column 
        self.recommend['rating'] = li_rating    # add " rating " column

p1 = MyData()        
p1.load_all_movies() 
p1.load_movie_ratings() 

### Insertion in 
@app.route('/', methods=['POST', 'GET'])  # Defines URL routing
def index():
    if request.method == 'POST':
        movieIdBy_user = request.form['content']
        print("User Requested for ID  : ",(movieIdBy_user))
        c=0
        for i in p1.all_movie.index:
            if p1.all_movie['item_id'][i] == int(movieIdBy_user) :
                p1.rows[0] = p1.all_movie['item_id'][i]
                p1.rows[1] = p1.all_movie['title'][i]
                p1.rows[2] = p1.all_movie['genres'][i]
                print("hello",p1.rows[0],p1.rows[1],p1.rows[2])
                c=1
        if c==0: # If no movies found
            return "MovieID_NOT_FOUND_404"
        else:
            p1.fun(p1.rows[1])
            p1.add_itemid_and_rating_coloumn()     
            return render_template('recommend.html',tasks=p1)
    else:
        # Website opens from here it renders the "index.html" page 
        # p1 has (p1.all_movie = pd.read_csv('movies.csv')) 
        return render_template('index.html',tasks=p1)

@app.route('/click/<int:item>')
def click(item):
    c=0
    for i in p1.all_movie.index:
        if p1.all_movie['item_id'][i] == item :
            p1.rows[0] = p1.all_movie['item_id'][i]
            p1.rows[1] = p1.all_movie['title'][i]
            p1.rows[2] = p1.all_movie['genres'][i]
            print("hello",p1.rows[0],p1.rows[1],p1.rows[2])
            c=1
    if c==1:                # Movie ID found in our CSV file 
        p1.fun(p1.rows[1])  # fun() will call 'recommend_movie()' in  " movie_recommendation.py "
        p1.add_itemid_and_rating_coloumn()  
        return render_template('recommend.html',tasks=p1)
    else:
        return "MovieID_NOT_FOUND_404"

if __name__=="__main__":       
    app.run(debug=True)        # helps run app on local deployment server
                               #    app.run( host , port , debug , options )