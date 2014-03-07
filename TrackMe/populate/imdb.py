import re
import sqlite3 as lite

# ftp://ftp.fu-berlin.de/pub/misc/movies/database/movies.list.gz
con = lite.connect('database.db')
cur = con.cursor()    

with open("movies.list","r") as f:
    for idx,line in enumerate(f):
        if(idx > 15):
#            print re.search('".*?"',line).group(0)                    #name
            #print re.search("\(.*\)",line).group(0).split(" ")[0]    #year
            try:
                name = re.search('".*?"',line)
                if name is not None and not '{' in line:
                    name = name.group(0).replace("\"","")
                    name = re.sub('[^0-9a-zA-Z ]+', '', name)
                    cur.execute('INSERT OR REPLACE INTO trackapp_trackable(name,item_type,description,amount,release_date,average_num_stars,total_views,plus_ones,cover_photo) VALUES ("'+name +'","tv","Fighting Soul Fighters",1234,2014-02-02,3,13352,25,"")')
            except lite.Error, e:
                print e.args[0] + " line: " + str(idx)
                con.close()
                break
con.commit()
con.close()
print "ok"