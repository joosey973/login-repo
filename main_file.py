from flask import Flask, render_template, request
from form import LoginForm
from data.db_session import global_init, create_session
from data.users import User


application = Flask(__name__)
application.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    application.run(host="127.0.0.1", port=8080)


@application.route("/", methods=['POST', 'GET'])
def main_page():
    form = LoginForm()
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            return render_template("login.html", title='Регистрация', form=form, message='Пароли не совпадают.')
        global_init("db/mars.explorers.db")
        session = create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('login.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть.")
        user = User()
        user.email = form.email.data
        user.name = form.name.data
        user.surname = form.surname.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return "You've successfully logined"
    return render_template('login.html', title='Регистрация', form=form)


if __name__ == "__main__":
    main()
