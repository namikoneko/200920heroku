from flask import Flask,render_template,request,redirect,url_for
import os
import dataset
import time
from datetime import date,datetime

db = dataset.connect('sqlite:///test.db')
'''
db_uri = os.environ.get('DATABASE_URL')
db = dataset.connect(db_uri)
'''

app = Flask(__name__)

# tag ============================================================
@app.route('/tag/list')
def taglist():
    rows = db['tag'].find(order_by='-updated')
    return render_template('taglist.html',rows=rows)

@app.route('/tag/ins_exe',methods=['POST'])
def tagins_exe():
    title = request.form['title']
    mydate = date.today().strftime('%Y-%m-%d')
    updated = time.time()
    table = db['tag']
    table.insert(dict(title=title, date=mydate, updated=updated))

    return redirect(url_for('taglist'))

@app.route('/tag/<id>')
def tagsingle(id):
    maprows = db['map'].find(tagid=id)

    threadids = []
    for maprow in maprows:
        threadids.append(maprow['threadid'])

    rows = db['thread'].find(id=threadids)

    tag = db['tag'].find_one(id=id)

    return render_template('tag.html',rows=rows,tag=tag)

@app.route('/tag/upd/<id>')
def tagupd(id):
    row = db['tag'].find_one(id=id)
    return render_template('tagupd.html',row=row)

@app.route('/tag/upd_exe',methods=['POST'])
def tagupd_exe():
    id = request.form['id']
    title = request.form['title']
    data = dict(id=id, title=title)
    table = db['tag']
    table.update(data, ['id'])
    return redirect(url_for('tagsingle',id=id))

@app.route('/tag/del/<id>')
def tagdel(id):
    table = db['tag']
    table.delete(id=id)
    return redirect(url_for('taglist'))

@app.route('/tag/up/<id>')
def tagup(id):
    table = db['tag']
    row = table.find_one(id=id)
    updated = time.time()
    data = dict(id=id, updated=updated)
    table.update(data, ['id'])
    return redirect(url_for('taglist'))

@app.route('/tag/up/<id>')
def tagup(id):
    table = db['tag']
    row = table.find_one(id=id)
    updated = time.time()
    data = dict(id=id, updated=updated)
    table.update(data, ['id'])
    return redirect(url_for('taglist'))

# cat ============================================================
@app.route('/cat/list')
def catlist():
    rows = db['cat'].find(order_by='-updated')
    return render_template('catlist.html',rows=rows)

@app.route('/cat/ins_exe',methods=['POST'])
def catins_exe():
    title = request.form['title']
    mydate = date.today().strftime('%Y-%m-%d')
    updated = time.time()
    table = db['cat']
    table.insert(dict(title=title, date=mydate, updated=updated))

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
    updated = time.time()
    table = db['post']
    table.insert(dict(title=title, date=mydate, updated=updated))

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
    rowBs = table.find(id={'!=':row['catid']},order_by='-updated')
    #rowBs = db.query("select * from post where catid != " + row['catid'] + " order by updated desc")
    #rowBs = db.query("select * from cat where id != 1 order by updated desc")
    #rowBs = db.query('select * from cat where id != ' + str(row["catid"]) + ' order by updated desc')

    return render_template('postupdcat.html',row=row,rowAs=rowAs,rowBs=rowBs)

@app.route('/post/updcat_exe/<catid>/<postid>')
def postupdcat_exe(catid,postid):
    table = db['post']

    data = dict(id=postid, catid=catid)
    table.update(data, ['id'])

    return redirect(url_for('postupdcat',id=postid))

# map ============================================================
@app.route('/map/add/<tagid>/<threadid>')
def mapadd(tagid,threadid):
    tagid = tagid
    threadid = threadid
    mydate = date.today().strftime('%Y-%m-%d')
    updated = time.time()
    table = db['map']
    table.insert(dict(tagid=tagid, threadid=threadid, date=mydate, updated=updated))

    return redirect(url_for('threadsingle',id=threadid))

@app.route('/map/del/<mapid>/<threadid>')
def mapdel(mapid,threadid):
    table = db['map']
    table.delete(id=mapid)
    return redirect(url_for('threadsingle',id=threadid))

# thread ============================================================
@app.route('/thread/<id>')
def threadsingle(id):
    row = db['thread'].find_one(id=id)

    joinrows = db.query('SELECT tag.id as tag_id, tag.title, map.id as map_id, map.threadid as map_threadid FROM tag join map on tag.id = map.tagid where map.threadid=' + str(id) + ' order by tag.updated desc')

    #使用されているtagのtagテーブルのidを配列で取得
    usedtagids = []
    for joinrow in joinrows:
        usedtagids.append(joinrow['tag_id']) 

    #すべてのtagのtagテーブルのidを配列で取得
    tagids = []
    tagrows = db['tag']
    for tagrow in tagrows:
        tagids.append(tagrow['id'])#tagのすべてのid 

    #集合の差を取得
    usedtagids_set = set(usedtagids)
    tagids_set = set(tagids)
    nousetags_set = tagids_set - usedtagids_set#集合の差を取得
    nousetags = list(nousetags_set)
    nouserows = db['tag'].find(id=nousetags)#使っていないtagを配列で検索

    joinrows = db.query('SELECT tag.id as tag_id, tag.title, map.id as map_id, map.threadid as map_threadid FROM tag join map on tag.id = map.tagid where map.threadid=' + str(id) + ' order by tag.updated')

    return render_template('thread.html',row=row,nouserows=nouserows,joinrows=joinrows)

'''
    usedtagids = []
    maprows = db['map'].find(threadid=id)#threadidでmapを検索

    for maprow in maprows:
        usedtagids.append(maprow['tagid'])#mapのtagidを配列に

    usedrows = db['tag'].find(id=usedtagids)#tagを配列で検索
'''

@app.route('/thread/ins_exe',methods=['POST'])
def threadins_exe():
    id = request.form['id']
    text = request.form['text']
    mydate = date.today().strftime('%Y-%m-%d')
    updated = time.time()
    table = db['thread']
    table.insert(dict(postid=id, text=text, date=mydate, updated=updated))

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
    app.debug = True
    app.run(host='0.0.0.0')
