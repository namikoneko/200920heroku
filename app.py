from flask import Flask,render_template,request,redirect,url_for
import os
import dataset
import time
from datetime import date,datetime

'''
db = dataset.connect('sqlite:///test.db')
'''
db_uri = os.environ.get('DATABASE_URL')
db = dataset.connect(db_uri)

app = Flask(__name__)

# cat ============================================================
@app.route('/cat/list')
def catlist():
    rows = db['cat'].find(order_by='-updated')
    return render_template('catlist.html',rows=rows)

@app.route('/cat/ins_exe',methods=['POST'])
def catins_exe():
    title = request.form['title']
    mydate = date.today().strftime('%Y-%m-%d')
    table = db['cat']
    table.insert(dict(title=title, date=mydate))

    return redirect(url_for('catlist'))

@app.route('/cat/<id>')
def catsingle(id):
    table = db['post']
    rows = table.find(catid=id)

    table = db['cat']
    cat = table.find_one(id=id)

    return render_template('cat.html',rows=rows,cat=cat)

@app.route('/cat/upd/<id>')
def catupd(id):
    table = db['cat']
    row = table.find_one(id=id)
    return render_template('catupd.html',row=row)

@app.route('/cat/upd_exe',methods=['POST'])
def catupd_exe():
    id = request.form['id']
    title = request.form['title']
    data = dict(id=id, title=title)
    table = db['cat']
    table.update(data, ['id'])
    return redirect(url_for('catsingle',id=id))

@app.route('/cat/del/<id>')
def catdel(id):
    table = db['cat']
    table.delete(id=id)
    return redirect(url_for('catlist'))

@app.route('/cat/up/<id>')
def catup(id):
    table = db['cat']
    row = table.find_one(id=id)
    updated = time.time()
    data = dict(id=id, updated=updated)
    table.update(data, ['id'])
    return redirect(url_for('catlist'))

# post ============================================================
@app.route('/post/list')
def postlist():
    rows = db['post'].find(order_by='-updated')
    return render_template('postlist.html',rows=rows)

@app.route('/post/<id>')
def postsingle(id):
    table = db['thread']
    rows = table.find(postid=id, order_by='-updated')

    table = db['post']
    post = table.find_one(id=id)

    table = db['cat']
    cats = table.find(id=post['catid'], order_by='-updated')

    return render_template('post.html',rows=rows,post=post,cats=cats)

@app.route('/post/ins_exe',methods=['POST'])
def postins_exe():
    title = request.form['title']
    mydate = date.today().strftime('%Y-%m-%d')
    table = db['post']
    table.insert(dict(title=title, date=mydate))

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

@app.route('/post/up/<id>')
def postup(id):
    table = db['post']
    row = table.find_one(id=id)
    updated = time.time()
    data = dict(id=id, updated=updated)
    table.update(data, ['id'])
    return redirect(url_for('postlist'))

@app.route('/post/updcat/<id>')
def postupdcat(id):
    table = db['post']
    row = table.find_one(id=id)

    table = db['cat']
    rowAs = table.find(id=row['catid'],order_by='-updated')
    #rowBs = table.find(id!=row['catid'],order_by='-updated')
    #rowBs = db.query("select * from post where catid != " + row['catid'] + " order by updated desc")
    #rowBs = db.query("select * from cat where id != 1 order by updated desc")
    rowBs = db.query('select * from cat where id != ' + str(row["catid"]) + ' order by updated desc')

    return render_template('postupdcat.html',row=row,rowAs=rowAs,rowBs=rowBs)

@app.route('/post/updcat_exe/<catid>/<postid>')
def postupdcat_exe(catid,postid):
    table = db['post']

    data = dict(id=postid, catid=catid)
    table.update(data, ['id'])

    return redirect(url_for('postupdcat',id=postid))

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
    mydate = date.today().strftime('%Y-%m-%d')
    table = db['thread']
    table.insert(dict(postid=id, text=text, date=mydate))

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
    row = table.find_one(id=id)
    table = db['thread']
    table.delete(id=id)
    postid = row['postid']
    return redirect(url_for('postsingle',id=postid))

@app.route('/thread/up/<id>')
def threadup(id):
    table = db['thread']
    row = table.find_one(id=id)
    postid = row['postid']
    updated = time.time()
    data = dict(id=id, updated=updated)
    table.update(data, ['id'])
    return redirect(url_for('postsingle',id=postid))

#============================================================
@app.route('/')
def hello():
    return "hello"

if __name__ == '__main__':
    #app.debug = True
    app.run(host='0.0.0.0')
