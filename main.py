# https://github.com/ipapMaster/flaskLessons
from flask import Flask, url_for, request, redirect
from flask import render_template, make_response
import json
import requests
from sqlalchemy.orm import sessionmaker
from loginform import LoginForm
from data import db_session
from mail_sender import send_mail
from dotenv import load_dotenv
from data.users import User
from data.news import News
from forms.user import RegisterForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'too short key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/news.sqlite'


# ошибка 404
@app.errorhandler(404)
def http_404_error(error):
    return redirect('/error404')


@app.route('/error404')
def well():  # колодец
    return render_template('well.html')


@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private !=True)
    # param = {}
    # param['username'] = 'Слушатель'
    # param['title'] = 'Расширяем шаблоны'
    return render_template('index.html', title='Новости', news=news)


@app.route('/odd_even')
def odd_even():
    return render_template('odd_even.html', number=3)


@app.route('/news')
def news():
    with open("news.json", "rt", encoding="utf-8") as f:
        news_list = json.loads(f.read())
    return render_template('news.html',
                           title='Новости',
                           news=news_list)
    # lst = ['ANN', 'TOM', 'BOB']
    # return render_template('news.html', title="FOR", news=lst)


@app.route('/vartest')
def vartest():
    return render_template('var_test.html', title='Переменные в HTML')


@app.route('/slogan')
def slogan():
    return 'Ибо крепка, как смерть, любовь!<br><a href="/">Назад</a>'


@app.route('/success')
def success():
    return 'Success'


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='проблемы с регистрацией', message='пароли не совпадают',
                                   form=form)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='проблемы с регистрацией', message='почта уже зарегина',
                                   form=form)
        user = User(name=form.name.data, email=form.email.data, about=form.about.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html',
                           title='Авторизация',
                           form=form)


@app.route('/weather_form', methods=['GET', 'POST'])
def weather_form():
    if request.method == 'GET':
        return render_template('weather_form.html',
                               title='Выбор города')
    elif request.method == 'POST':
        town = request.form.get('town')
        data = {}
        key = 'c747bf84924be997ff13ac5034fa3f86'
        url = 'http://api.openweathermap.org/data/2.5/weather'
        params = {'APPID': key, 'q': town, 'units': 'metric'}
        result = requests.get(url, params=params)
        weather = result.json()
        code = weather['cod']
        icon = weather['weather'][0]['icon']
        temperature = weather['main']['temp']
        data['code'] = code
        data['icon'] = icon
        data['temp'] = temperature
        return render_template('weather.html',
                               title=f'Погода в городе {town}',
                               town=town, data=data)


@app.route('/form_sample', methods=['GET', 'POST'])
def form_sample():
    if request.method == 'GET':
        return render_template('user_form.html', title='Форма')
    elif request.method == 'POST':
        f = request.files['file']  # request.form.get('file')
        f.save('./static/images/loaded.png')
        myform = request.form.to_dict()
        return render_template('filled_form.html',
                               title='Ваши данные',
                               data=myform)


@app.route('/load_photo', methods=['GET', 'POST'])
def load_photo():
    if request.method == 'GET':
        return f"""
        <form class="login_form" method="post" enctype="multipart/form-data">
            <div class="form-group">
                <label for="photo">Приложите фото:</label>
                <input type="file" class="from-control-file" id="photo" name="file">
            </div><br>
            <button type="submit" class="btn btn-primary">Отправить</button>
        </form>
        """
    elif request.method == 'POST':
        f = request.files['file']  # request.form.get('file')
        f.save('./static/images/loaded.png')
        return '<h1>Файл у Вас на сервере</h1>'

@app.route('/cookie_test')
def cookie_test():
    visit_count = int(request.cookies.get('visit_count', 0))
    if visit_count:
        res = make_response(f' посещений {visit_count + 1}')
        res.set_cookie('visit_count', str(visit_count +1), max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response('вы впервые здесь за 2 года')
        res.set_cookie('visit_count', '1', max_age=60 * 60 * 24 * 365 * 2)
    return res



@app.route('/mail', methods=['GET'])
def get_form():
    return render_template('mail_send.html')


@app.route('/mail', methods=['POST'])
def post_form():
    email = request.values.get('email')
    if send_mail(email, 'Вам письмо', 'Текст письма'):
        return f'Письмо на адрес {email} отправлено успешно!'
    return 'Сбой при отправке'


if __name__ == '__main__':
    db_session.global_init('db/news.sqlite')
    app.run(host='127.0.0.1', port=5000, debug=True)
    # user = User()
    # user.name = 'Mixa'
    # user.about = 'santexnik'
    # user.email ='tvv11@mail.ru'
    # db_sess = db_session.create_session()
    # db_sess.add(user)
    # db_sess.commit()
    # работу с БД начинают  с открытия сессии
    # db_sess = db_session.create_session()
    # user = db_sess.query(User).filter(User.id).first()
    # subj = News(title = 'Новость от Владимра номер 1', content='Пошел на обед',
    #             is_private=False)
    # db_sess.add(news)
    # user.news.append(subj)
    # db_sess.commit()
    # с помощью обьекта сессии происходит обращение к таблицам
    # user = db_sess.query(User).first()
    # print(user)
    # print(user.name)
    # print(user.email)
    # users = db_sess.query(User).all()
    # for user in users:
    #     print(user)
    # users = db_sess.query(User).filter(User.id > 1)
    # for user in users:
    #     print(user)
# | или -  в сложных запросах
# & и  -  в сложных запросах