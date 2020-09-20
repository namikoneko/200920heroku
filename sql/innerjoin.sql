--SELECT * from (SELECT * FROM map m left join thread thr on thr.mapid = m.id) join tag on tagid = tag.id;
SELECT tag.id as tag_id,tag.title as tag_title, map_id from (SELECT m.id as map_id,m.tagid as map_tagid FROM map m left join thread thr on thr.mapid = map_id) join tag on map_tagid = tag.id;
