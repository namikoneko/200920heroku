from flask import Flask,render_template,request,redirect,url_for
import os
import dataset

app = Flask(__name__)

db = dataset.connect('sqlite:///test.db')
'''
db_uri = os.environ.get('DATABASE_URL')
db = dataset.connect(db_uri)
'''

@app.route('/thread/<id>')
def thread(id):
    table = db['thread']
    row = table.find_one(id=id)
    return render_template('thread.html',row=row)

@app.route('/')
def hello():
    return "hello"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
