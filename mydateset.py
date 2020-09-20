from flask import Flask,render_template,request,redirect,url_for
from datetime import date,datetime
import os
import dataset
import time

db = dataset.connect('sqlite:///test.db')

app = Flask(__name__)

@app.route('/dict/<id>')
def mydict(id):
    maptagids = []
    maprows = db['map'].find(threadid=id)#threadidでmapを検索

    for maprow in maprows:
        maptagids.append(maprow['tagid'])#mapのtagidを配列に

    tagrows = db['tag'].find(id=maptagids)#tagを配列で検索

    #joinrows = db.query('SELECT tag.id as tag_id, tag.title, map.id as map_id FROM tag join map on tag.id = map.tagid')
    joinrows = db.query('SELECT tag.id as tag_id, tag.title, map.id as map_id FROM tag join map on tag.id = map.tagid where tag.id=' + str(id))

    tagids = []
    tagrows = db['tag']
    for tagrow in tagrows:
        tagids.append(tagrow['id'])#tagのすべてのid 

    maptagids_set = set(maptagids)
    tagids_set = set(tagids)
    nousetags_set = tagids_set - maptagids_set#集合の差を取得
    nousetags = list(nousetags_set)
    nouserows = db['tag'].find(id=nousetags)#使っていないtagを配列で検索

    return render_template('test.html',tagrows=tagrows,nouserows = nouserows,joinrows=joinrows)

@app.route('/not')
def mynot():
    table = db['foo']
    #winners = db.query('SELECT b FROM foo intersect select b from bar')
    #winners = db.query('SELECT b FROM foo except select b from bar')
    #winners = db.query("SELECT b FROM foo where b not in ('B','C')")
    agroup = table.find(id=[1, 3])
    bgroup = table
    winners = db.query('SELECT tag.id as tag_id,tag.title as tag_title, map_id from (SELECT m.id as map_id,m.tagid as map_tagid FROM map m left join thread thr on thr.mapid = map_id) join tag on map_tagid = tag.id')
    tagall = db.query('SELECT tag.id as tag_id,tag.title as tag_title, map.id as map_id from tag left join map on map.tagid = tag.id')
    #myexcepts = db.query('SELECT tag.id as tag_id,tag.title as tag_title, map.id as map_id from tag left join map on map.tagid = tag.id except SELECT tag.id as tag_id,tag.title as tag_title, map_id from (SELECT m.id as map_id,m.tagid as map_tagid FROM map m left join thread thr on thr.mapid = map_id) join tag on map_tagid = tag.id')
    myexcepts = db.query('SELECT tag.id as tag_id,tag.title as tag_title, map.id as map_id from tag left join map on map.tagid = tag.id except SELECT tag.id,tag.title, map_id from (SELECT m.id as map_id,m.tagid as map_tagid FROM map m left join thread thr on thr.mapid = map_id) join tag on map_tagid = tag.id')

    #return render_template('test.html',winners=agroup)
    return render_template('test.html',winners=winners,tagall=tagall,myexcepts=myexcepts)
    #for winner in table:
    #    bgroup.append(winner['b'])

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
