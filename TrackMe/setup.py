import os
import sqlite3 as lite


#populate trackables
#os.system("python populate/anidb.py")


con = lite.connect('database.db')
cur = con.cursor()    
cur.execute('insert into trackapp_background (obj) VALUES ("background/background.jpg")')
con.commit()
con.close()
