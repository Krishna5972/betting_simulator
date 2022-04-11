from flask import Flask,render_template
from os import environ

app=Flask(__name__)


open_bet_ids=[1,4,21,99]

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html',open_bet_ids=open_bet_ids,title='Index')

@app.route('/about')
def about():
    return render_template('about.html',title='About')


def main():
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT,debug=True)
    
if __name__ == '__main__':
    main()

