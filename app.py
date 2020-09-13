from flask import Flask,render_template,request,redirect,url_for
import os
import dataset

app = Flask(__name__)

db = dataset.connect('sqlite:///test.db')
'''
db_uri = os.environ.get('DATABASE_URL')
db = dataset.connect(db_uri)
'''

# post ============================================================
@app.route('/post/<id>')
def postsingle(id):
    statement = 'select post.title as ptitle from post inner join thread using (id)'
    #statement = 'select post.id as pid post.title as ptitle thread.id as tid thread.text as ttext from post inner join thread using (id)'
    rows = db.query(statement)
    #post = rows.first()
    return render_template('post.html',rows=rows)
    #return render_template('post.html',rows=rows,post=post)

# thread ============================================================
@app.route('/thread/<id>')
def threadsingle(id):
    table = db['thread']
    row = table.find_one(id=id)
    return render_template('thread.html',row=row)

@app.route('/thread/upd/<id>')
def threadupd(id):
    table = db['thread']
    row = table.find_one(id=id)
    return render_template('threadupd.html',row=row)

@app.route('/thread/upd_exe',methods=['POST'])
def threadupd_exe():
    id = request.form['id']
    text = request.form['text']
    data = dict(id=id, text=text)
    table = db['thread']
    table.update(data, ['id'])
    return redirect(url_for('threadsingle',id=id))

@app.route('/thread/del/<id>')
def threaddel(id):
    table = db['thread']
    table.delete(id=id)
    return redirect(url_for('postsingle',id=row.postid))
#============================================================
@app.route('/')
def hello():
    return "hello"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
