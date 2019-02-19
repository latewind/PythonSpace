from flask import Flask
from flask_bootstrap import Bootstrap
from flask import render_template

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return '<div>Index</div>'


@app.route('/user')
def user():
    return render_template('user.html', name="Tom")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12800,debug=True)
