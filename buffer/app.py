from flask import Flask, render_template, redirect, url_for, session, request, flash, Markup
from flask_sqlalchemy import SQLAlchemy
import hashlib, datetime
from werkzeug.utils import secure_filename
import os
# os.chdir('/var/www/FlaskApp/App/')
UPLOAD_FOLDER = './static/images/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = "kakwdk982ukiajkds"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
salt = "kfjwej2849"


#DB Config
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qhgvwsermimino:79f72da5cc5ca92807334413bee6c19ba90739403d7da342c24e8c43ae663468@ec2-54-72-155-238.eu-west-1.compute.amazonaws.com:5432/df4ai5d5tpa1mo'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

#Database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    passhash = db.Column(db.String)
    name = db.Column(db.String)

class UserActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    activity = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer)
    featured_image_uri = db.Column(db.String)
    article_title = db.Column(db.String)
    article_body = db.Column(db.String)
    is_published = db.Column(db.Boolean)


@app.route('/')
def index():
    return render_template('index-4.html')

@app.route('/int-article')
def intArticle():
    return render_template('int_article.html')

@app.route('/wip')
def wip():
    return render_template('index-uw.html')

@app.route('/cdn', methods=['GET', 'POST'])
def cdn():
    if request.method == 'POST':
        if request.form.get('email'):
            user = User.query.filter_by(email=request.form.get('email')).first()
            if user is not None:
                passhash = hashlib.md5(request.form.get('password').encode())
                if user.passhash == passhash.hexdigest():
                    session['logged_in'] = True
                    session['user_id'] = user.id
                    activity = UserActivity(user_id=user.id, activity="Logged in to CDN.")
                    db.session.add(activity)
                    db.session.commit()
                    return redirect(url_for('cdnControlpanel'))
                else:
                    flash('Feil epost/passord.')
                    return render_template('cdn.html')
            else:
                flash('Feil epost/passord.')
                return render_template('cdn.html')
        else:
            flash('Feil epost/passord.')
            return render_template('cdn.html')
    elif request.method == 'GET':
        if session.get('logged_in'):
            return redirect(url_for('cdnControlpanel'))
        else:
            return render_template('cdn.html')

@app.route('/cdn-controlpanel', methods=['GET', 'POST'])
def cdnControlpanel():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filenamea
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(request.url)

    elif request.method == 'GET':
        if session.get('logged_in'):
            directory = './static/images/'
            urls = []
            for filename in os.listdir(directory):
                if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
                    urls.append(os.path.join(directory, filename))
                else:
                    continue
            return render_template('cdn.controlpanel.html', urls=urls, user=User.query.filter_by(id=session['user_id']).first())


@app.route("/cdn-editor")
def cdnEditor():
    if session.get('logged_in'):
        print(User.query.filter_by(id=session['user_id']).first().name)
        return render_template("cdn.editor.html", user=User.query.filter_by(id=session['user_id']).first())
    else:
        return redirect(url_for('cdn'))


@app.route("/cdn-profile")
def cdnProfile():
    if request.method == "POST":
        pass
    elif request.method == "GET" and session.get('logged_in'):
        return render_template('cdn.profile.html', user=User.query.filter_by(id=session['user_id']).first())
    else:
        return redirect(url_for('cdn'))

@app.route("/article-upload", methods = ['GET', 'POST'])
def articleUpload():
    if request.method == "POST" and session.get('logged_in'):
        fUrl = request.form.get('featureUrl')
        title = request.form.get('title')
        content = request.form.get('content')
        published = request.form.get('published')
        if published == "true":
            published = True
        else:
            published = False
        article = Article(author_id=session.get('user_id'),featured_image_uri=fUrl, article_title=title, article_body=content, is_published=published)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('cdnEditor'))


@app.route('/article', methods=['GET', 'POST'])
def article():
    if request.method == "GET":
        aid = request.args.get('aid')
        article = Article.query.filter_by(id=aid).first()
    return render_template('article_body.html', article=article, articleContent=Markup(article.article_body))


@app.route('/logout')
def logout():
    session.pop('logged_in')
    session.pop('user_id')
    return redirect(url_for('index'))
