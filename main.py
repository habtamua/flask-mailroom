import os
# import base64

from flask import Flask, render_template, request, redirect, url_for, session
from passlib.hash import pbkdf2_sha256
from model import Donation, Donor, User

app = Flask(__name__)
app.secret_key = b'#\xce\xe7(>\xcf\xc8\xae\x1e\x7f\x82\xd3\xc8\x80\x18\x11w\xa5,\xf0\x990`~'


@app.route('/')
def home():
    return redirect(url_for('all'))


@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if request.method == 'POST':
        donor = Donor.select().where(Donor.name == request.form['name']).get()
        # donor = Donor(name=request.form['name'])
        donation = Donation(value=request.form['value'], donor=donor)
        donation.save()

        return redirect(url_for('all'))
    # else:
    return render_template('donate.jinja2')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.select().where(User.username == request.form['username']).get()

        if user and pbkdf2_sha256.verify(request.form['password'], user.password):
            session['username'] = request.form['username']
            return redirect(url_for('all'))

        return render_template('login.jinja2', error="Incorrect username or password")

    # else:
    return render_template('login.jinja2')


# @app.route('/view/')
# def view():
#     name = request.args.get('name', None)
#
#     if name is None:
#         return render_template('view.jinja2')
#     else:
#         try:
#             donor = Donor.get(Donor.name == name)
#         except Donor.DoesNotExist:
#             return render_template('view_jinja2', error="Donor does not exist")
#
#         donations = Donation.select().where(Donation.donor == donor)
#         total = 0
#         for donation in donations:
#             total += donation.value
#
#         return render_template("view.jinja2", donations=donations, name=donor.name, total=total)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
