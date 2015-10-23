

import psycopg2
from eveIntel.sqlinterface import sqlConnection
from eveIntel.sqlEnginePostgres import sqlEnginePostgres
from eveIntel.sqlEngineSqlite import sqlEngineSqlite

from eveIntel.dbpopulate import *

con = psycopg2.connect("""dbname= 'EveIntelDB' user='migration'
host='localhost' password='migration3606273887976070'""")


sqliteDB = sqlConnection()
sqliteDB.setSqlEngine(sqlEngineSqlite())
sqliteDB.connect()

postgres = sqlConnection()
#postgres.setSqlEngine(sqlEnginePostgres())
postgres.connect()
#sql.setConnection(con)
#sql.notSqlite()

def migrateRawMails():
    killsRaw = sqliteDB.sqlCommand("select zkillid, killmail from killsraw;")
    count=0
    total=len(killsRaw)
    print(str(total)+" total killsRaw")
    x=""
    for i in killsRaw:
        if(count%10000==0):
            print(str(count)+" mails processed out of: "+str(total))
            postgres.commit()
            #print(str(x))
            #print("\n"+str(i[1]))
        x=postgres.insertRawKM(i[0], i[1], commit=True)
        count=count+1
    postgres.commit()
    print("migration finished")
sql=postgres
migrateRawMails()
#processPulledKills()
    
