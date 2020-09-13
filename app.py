from flask import Flask,render_template,request,redirect,url_for
import os
import dataset

app = Flask(__name__)

'''
db = dataset.connect('sqlite:///test.db')
'''
db_uri = os.environ.get('DATABASE_URL')
db = dataset.connect(db_uri)

# post ============================================================
@app.route('/post/list')
def postlist():
    rows = db['post'].all()
    return render_template('postlist.html',rows=rows)

@app.route('/post/<id>')
def postsingle(id):
    table = db['thread']
    rows = table.find(postid=id)

    table = db['post']
    post = table.find_one(id=id)

    return render_template('post.html',rows=rows,post=post)

@app.route('/post/ins_exe',methods=['POST'])
def postins_exe():
    title = request.form['title']
    table = db['post']
    table.insert(dict(title=title))

    return redirect(url_for('postlist'))

@app.route('/post/upd/<id>')
def postupd(id):
    table = db['post']
    row = table.find_one(id=id)
    return render_template('postupd.html',row=row)

@app.route('/post/upd_exe',methods=['POST'])
def postupd_exe():
    id = request.form['id']
    title = request.form['title']
    data = dict(id=id, title=title)
    table = db['post']
    table.update(data, ['id'])
    return redirect(url_for('postsingle',id=id))

@app.route('/post/del/<id>')
def postdel(id):
    table = db['post']
    table.delete(id=id)
    return redirect(url_for('postlist'))
'''
'''

# thread ============================================================
@app.route('/thread/<id>')
def threadsingle(id):
    table = db['thread']
    row = table.find_one(id=id)
    return render_template('thread.html',row=row)

@app.route('/thread/ins_exe',methods=['POST'])
def threadins_exe():
    id = request.form['id']
    text = request.form['text']
    table = db['thread']
    table.insert(dict(postid=id, text=text))

    return redirect(url_for('postsingle',id=id))

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
