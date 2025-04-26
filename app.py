from flask import Flask, render_template


app = Flask(__name__, template_folder='application/templates',
            static_folder='application/static')


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/index')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
