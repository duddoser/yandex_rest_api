from flask import Flask, render_template, redirect, session, jsonify, make_response, request
from loginform import LoginForm
from usersmodel import UsersModel
from newsmodel import NewsModel
from add_news import AddNewsForm
from db import DB

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

db = DB()
UsersModel(db.get_connection()).init_table()
NewsModel(db.get_connection()).init_table()


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user_name = form.username.data
#         password = form.password.data
#         user_model = UsersModel(db.get_connection())
#         user_model.insert('login1', 'password1')
#         exists = user_model.exists(user_name, password)
#         if exists[0]:
#             session['username'] = user_name
#             session['user_id'] = exists[1]
#         return redirect('/index')
#     return render_template('login.html', title='Авторизация', form=form)


@app.route('/news',  methods=['GET'])
def get_news():
    news = NewsModel(db.get_connection()).get_all()
    return jsonify({'news': news})


@app.route('/news', methods=['POST'])
def create_news():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['title', 'content', 'user_id']):
        return jsonify({'error': 'Bad request'})
    news = NewsModel(db.get_connection())
    news.insert(request.json['title'], request.json['content'],
                request.json['user_id'])
    return jsonify({'success': 'OK'})


@app.route('/news/<int:news_id>',  methods=['GET'])
def get_one_news(news_id):
    news = NewsModel(db.get_connection()).get(news_id)
    if not news:
        return jsonify({'error': 'Not found'})
    return jsonify({'news': news})


@app.route('/news/<int:news_id>', methods=['PUT'])
def put_one_news(news_id):
    news = NewsModel(db.get_connection())
    if not news.get(news_id):
        return jsonify({'error': 'Not found'})
    if 'user_id' not in request.json:
        return jsonify({'error': 'Bad request'})
    if 'title' in request.json:
        news.put(request.json[str(news_id)], title=request.json['title'])
    elif 'content' in request.json:
        news.put(request.json[str(news_id)], content=request.json['content'])
    elif 'title' in request.json and 'content' in request.json:
        news.put(request.json[str(news_id)], title=request.json['title'], content=request.json['content'])
    return jsonify({'success': 'OK'})


@app.route('/news/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    news = NewsModel(db.get_connection())
    if not news.get(news_id):
        return jsonify({'error': 'Not found'})
    news.delete(news_id)
    return jsonify({'success': 'OK'})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# @app.route('/logout')
# def logout():
#     session.pop('username', 0)
#     session.pop('user_id', 0)
#     return redirect('/login')


# @app.route('/')
# @app.route('/index')
# def index():
#     if 'username' not in session:
#         return redirect('/login')
#     news = NewsModel(db.get_connection()).get_all(session['user_id'])
#     return render_template('index.html', username=session['username'],
#                            news=news)


# @app.route('/add_news', methods=['GET', 'POST'])
# def add_news():
#     if 'username' not in session:
#         return redirect('/login')
#     form = AddNewsForm()
#     if form.validate_on_submit():
#         title = form.title.data
#         content = form.content.data
#         nm = NewsModel(db.get_connection())
#         nm.insert(title, content, session['user_id'])
#         return redirect("/index")
#     return render_template('add_news.html', title='Добавление новости',
#                            form=form, username=session['username'])


# @app.route('/delete_news/<int:news_id>', methods=['GET'])
# def delete_news(news_id):
#     if 'username' not in session:
#         return redirect('/login')
#     nm = NewsModel(db.get_connection())
#     nm.delete(news_id)
#     return redirect("/index")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

