import re
import sqlite3 as lite

# ftp://ftp.fu-berlin.de/pub/misc/movies/database/movies.list.gz
con = lite.connect('database.db')
cur = con.cursor()    

used = []

with open("populate/anime-titles.dat","r") as f:
    for idx,line in enumerate(f):
        if(idx > 4):
            try:
                regexed = re.findall("[^|]*",line)
                pid = regexed[0]    #ids
                syn = regexed[2]
                lang = regexed[4]
                name = regexed[6]
                if name is not None and syn == "1":#not pid in used:    
                    used.append(pid)
                    name = name.replace("\"","")
                    cur.execute('INSERT OR REPLACE INTO trackapp_trackable(name,item_type,description,amount,release_date,average_num_stars,total_views,plus_ones,cover_photo) VALUES ("'+name +'","Anime","Fighting Soul Fighters",1234,2014-02-02,3,13352,25,"")')
            except lite.Error, e:
                print e.args[0] + " line: " + str(idx)
                con.close()
                break
con.commit()
con.close()
print "ok"