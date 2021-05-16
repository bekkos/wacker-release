from flask import Flask, render_template, url_for, redirect, request, session

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/article')
def article():
    if request.args.get('id') is None:
        return redirect(url_for('index'))
    id = request.args.get('id')
    string = "article" + str(id) + ".html"
    return render_template(string)

@app.route('/om-oss')
def omOss():
    return render_template('om-oss.html')