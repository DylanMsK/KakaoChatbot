from flask import Flask, jsonify, request, render_template
import random
import requests
from bs4 import BeautifulSoup
from sqlalchemy.sql.expression import func, select

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import *


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///movie'
# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


@app.route('/keyboard')
def keaboard():
    keyboard = {"type" : "buttons",
                "buttons" : ['메뉴', "로또", "고양이", '영화', '영화저장']
    }
    return jsonify(keyboard)
    
@app.route('/message', methods=['POST'])
def message():
    user_msg = request.json['content']
    img_bool = False
    
    
    if user_msg == '메뉴':
        menus = ['제육덮밥', '김까', '20층', '부대찌개']
        random_pick = random.choice(menus)
        msg = random_pick
    
    elif user_msg == '로또':
        num = list(range(1, 46, 1))
        picked = random.sample(num, 6)
        normal_picked = ', '.join(str(i) for i in sorted(picked[:-1]))
        bonus_picked = str(picked[-1])
        msg = '이번주 로또는 {}, 보너스번호 {}입니다.'.format(normal_picked, bonus_picked)
    
    elif user_msg == '고양이':
        img_bool = True
        cat_api = 'https://api.thecatapi.com/v1/images/search?mime_types=jpg'
        req = requests.get(cat_api).json()
        url = req[0]['url']
        msg = '커엽'

    elif user_msg == '영화':
        img_bool = True
        movie = db.session.query(Movie)[random.randrange(0, 5)]
        
        msg = '제목: {}\n평점: {}\n예매율: {}'.format(movie.title, movie.star, movie.ratio)
        url = movie.img
    
    elif user_msg == '영화저장':
        db.session.query(Movie).delete()
        db.session.commit()
        
        naver_movie = 'https://movie.naver.com/movie/running/current.nhn'
        html = requests.get(naver_movie).text
        soup = BeautifulSoup(html, 'html.parser')
        
        movies = soup.select('div.lst_wrap > ul.lst_detail_t1 > li')[:5]
        movie_lst = []
        
        for movie in movies:
            movie_dict = {'title': None, 'star': None, 'ratio': None, 'img': None}
            movie_dict['title'] = movie.select_one('dt.tit > a').text
            movie_dict['star'] = movie.select_one('div.star_t1 > a > span.num').text
            movie_dict['ratio'] = movie.select_one('div.star_t1.b_star > span.num').text
            movie_dict['img'] = movie.find('div', class_='thumb').find('img')['src']
            # movie_dict['url'] = movie.select_one('div.thumb > img')['src']
            movie_lst.append(movie_dict)
        
        for movie in movie_lst:
            temp = Movie(
                movie['title'],
                movie['star'],
                movie['ratio'],
                movie['img']
                )
            db.session.add(temp)
            db.session.commit()
        
        msg = '저장완료'
        
    
    if img_bool:
        return_img_dict = {
            'message':{
                'text': msg,
                'photo':{
                    'url': url,
                    'width': 720,
                    'height': 630
                    }
                },
            'keyboard':{
                "type":"buttons",
                "buttons":['메뉴', "로또", "고양이", '영화', '영화저장']
            }
        }
        return jsonify(return_img_dict)
    else:
        return_dict = {
            'message':{
                'text': msg
            },
            'keyboard':{
                "type":"buttons",
                "buttons":['메뉴', "로또", "고양이", '영화', '영화저장']
            }
        }
        return jsonify(return_dict)