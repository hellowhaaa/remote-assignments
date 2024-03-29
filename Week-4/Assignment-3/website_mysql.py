import pymysql.cursors
from flask import Flask, render_template, request, redirect, url_for
import re

db = pymysql.connect(host='localhost',
                     user='root',
                     password='password123',
                     database='assignment',
                     cursorclass=pymysql.cursors.DictCursor)
my_cursor = db.cursor()
app = Flask(__name__)
app.secret_key = 'dfssdgfgd'
regex = re.compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")


def is_valid(email):
    if re.fullmatch(regex, email):
        return True
    else:
        return False


@app.route('/')
def homepage():
    wrong = request.args.get('wrong')
    return render_template('homepage.html', wrong=wrong)


@app.route('/member', methods=['GET', 'POST'])
def member():
    email = request.form.get('email')
    password = request.form.get('password')
    if request.method == 'POST':
        if request.values['send'] == 'submit-sign-in':  # if button's value is submit-sign-in
            query1 = "SELECT `email` FROM `user` WHERE `email`=%s AND `password`=%s"
            my_cursor.execute(query1, (email, password))
            if my_cursor.fetchone() is None:
                wrong = 'Your email or password is wrong'
                return redirect(url_for('homepage', wrong=wrong))
            else:
                return render_template('member.html', email=email)
        else:  # if button's value is submit-sign-up
            query2 = "SELECT `email` FROM `user` WHERE `email`=%s"
            my_cursor.execute(query2, email)
            if my_cursor.fetchone():
                wrong = 'The email address has been used!'
                return redirect(url_for('homepage', wrong=wrong))
            else:
                if is_valid(email):
                    query3 = "INSERT INTO `user`(`email`, `password`) VALUES (%s, %s)"
                    my_cursor.execute(query3, (email, password))
                    db.commit()
                    return render_template('member.html', new_email=email)
                else:
                    wrong = 'The email address is invalid!'
                    return redirect(url_for('homepage', wrong=wrong))


if __name__ == '__main__':
    app.run(debug=True, port=4600)
