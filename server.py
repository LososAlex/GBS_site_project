from flask import Flask, request, render_template, redirect, session, jsonify
from flask_restful import reqparse, abort, Api, Resource
from requests import get
from add_news import AddNewsForm
from loginform import LoginForm
from signupform import SignUpForm
from db import DB, NewsModel, UserModel

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'Project_GBS_secret_key'
db = DB()
user_model = UserModel(db.get_connection())
news_model = NewsModel(db.get_connection())


def abort_if_news_not_found(news_id):
    if not NewsModel(db.get_connection()).get(news_id):
        abort(404, message="News {} not found".format(news_id))


class News(Resource):
    def get(self, news_id):
        abort_if_news_not_found(news_id)
        news = NewsModel(db.get_connection()).get(news_id)
        return jsonify({'news': news})

    def delete(self, news_id):
        abort_if_news_not_found(news_id)
        NewsModel(db.get_connection()).delete(news_id)
        return jsonify({'success': 'OK'})


api.add_resource(News, '/get_news/<int:news_id>')


@app.route('/')
def home():
    news = news_model.get_all()
    return render_template('main.html', title='Главная', news=news)


@app.route('/about')
def about():
    return render_template('about.html', title='О нас')


@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    form = AddNewsForm()
    if request.method == 'GET':
        if 'username' not in session:
            return redirect('/login')
        return render_template('add_news.html', title='Добавить новость', form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            project = form.project.data
            try:
                f = request.files['image']
                filename = f.filename
                file = open('static\\img\\news\\{}'.format(f.filename), 'wb')
                file.write(f.read())
                file.close()
            except:
                filename = None
            news_model.insert(session['user_id'], title, content, filename, project)
            return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        exists = user_model.exists(user_name, password=password)
        if exists[0]:
            session['username'] = user_name
            session['user_id'] = exists[1]
            session['permission'] = exists[2]
            return redirect("/")
        else:
            return redirect('/login_error')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    session.pop('permission', 0)
    return redirect('/login')


@app.route('/login_error')
def login_error():
    return render_template('login_error.html', title='Ошибка')


@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        if user_model.exists(user_name):
            error = 'Пользователь с таким логином уже существует'
            return render_template('signup.html', title='Регистрация', form=form, error_login=error)
        else:
            user_model.insert(user_name, password, 'user')
            return render_template('success.html', title='Успешно')
    return render_template('signup.html', title='Регистрация', form=form, error_login=None)


@app.route('/profile')
def profile():
    return render_template('profile.html', title='Профиль')


@app.route('/projects')
def projects():
    return render_template('projects.html', title='Проекты')


@app.route('/Catch_The_Key')
def CTK():
    news = news_model.get_all('CTK')
    return render_template('CTK.html', news=news, title='Catch The Key')


@app.route('/Game_in_One_Level')
def GiOL():
    news = news_model.get_all('GiOL')
    return render_template('GiOL.html', news=news, title='Game in One Level')


@app.route('/The_Mountain')
def Mountain():
    news = news_model.get_all('TM')
    return render_template('Mountain.html', news=news, title='The Mountain')


@app.route('/delete_news/<int:news_id>', methods=['POST', 'GET'])
def delete_news(news_id):
    if session['permission'] != 'admin':
        return redirect('/')
    else:
        news_model.delete(news_id)
        return '<script>document.location.href = document.referrer</script>'


@app.route('/news/<int:news_id>')
def get_news(news_id):
    address = 'http://localhost:8000/get_news/{}'.format(news_id)
    news = get(address).json()['news']
    print(get(address).json()['news'])
    return render_template('news.html', item=news, title=news[2])


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')
