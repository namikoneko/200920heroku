from flask import Flask,render_template,request,redirect,url_for
from datetime import date,datetime
import os
import dataset
import time

app = Flask(__name__)

db = dataset.connect('sqlite:///test.db')

@app.route('/time')
def mytime():
    return str(time.time())
    #return date.today().strftime('%Y-%m-%d')

@app.route('/rows')
def rows():
    id=1
    table = db['thread']
    row = table.find_one(id=id)
    myint = row['postid']

    return str(myint)
    #return row

@app.route('/join')
def join():
    statement = 'select foo.b as b1,bar.b as b2 from foo inner join bar using (a)'
    rows = db.query(statement)

    return render_template('join.html',rows=rows)

'''
tests = db['test'].all()

for test in tests:
    print(test['title'])
'''

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
