

import sqlite3 as sql
import sys
import os


class sqlConnection():
    #con = None
    def __init__(self):
        
        #self.dbDir = "D:\\sqlite3"
        self.dbDir = "K:\\sqlite3"
        os.chdir(self.dbDir)
        self.dbName = "test.db"
        self.con = None
    def connect(self):
        self.con = sql.connect(self.dbName)
    def commit(self):
        self.con.commit()
    def close(self):
        self.con.close()
        
    def setDBDir(d):
        self.dbDir = d

    def __interactive(self):
        #
        os.chdir(dbDir)
        dbName = "test.db"
        con = sql.connect(dbName)    
        cur = con.cursor()
        print("Connected to DB: " + dbName)
        while(True):
            print("\nsql> " )
            command = str(raw_input())
            if(command =="exit" or command =="quit"):
                break
            try:
                cur.execute(command)
                con.commit()
                data = cur.fetchall()
                
                print(data)
                
            except sql.Error, e:
                print("Error %s:" % e.args[0])


        if con:
            con.close()


    def sqlCommand(self, command):
        #
            
        cur = self.con.cursor()
        try:
            cur.execute(command)
            self.con.commit()
            data = cur.fetchall()

            #if con:
                #con.close()
            return data
                
        except sql.Error, e:
            print("Error %s:" % e.args[0])
        #if con:
            #con.close()
        

    def sqlCommandParameterized(self, command, params):
        #
           
        cur = self.con.cursor()
        try:
            cur.execute(command, params)
            self.con.commit()
            data = cur.fetchall()

            #if con:
                #con.close()
            return data
                
        except sql.Error, e:
            return ("Error %s:" % e.args[0])

        #if con:
            #con.close()
    def sqlCommandParameterized2(self, command, params):
        #
           
        cur = self.con.cursor()
        try:
            cur.execute(command, params)
            #self.con.commit()
            data = cur.fetchall()

            #if con:
                #con.close()
            return data
                
        except sql.Error, e:
            return ("Error %s:" % e.args[0])

        #if con:
            #con.close()

        
    def insertRawKM(self, zkillID, rawKM):
        
        command="insert or ignore into killsRaw (zKillID, killmail, processed, skipped) values (?,?, 'False','False');"
        return self.sqlCommandParameterized(command, (zkillID, rawKM))

    def insertAlliance(self, ccpID, name):
        command = "insert or ignore into alliances (ccpID, name) values (?,?);"
        return self.sqlCommandParameterized(command, (ccpID, name))
    
    def insertCorp(self, ccpID, name, alliance=None):
        if(alliance is None):
            command = "insert or ignore into corporations (ccpID, name) values (?,?);"
            return self.sqlCommandParameterized(command, (ccpID, name)) 
        else:
            command = "insert or ignore into corporations (ccpID, name, alliance) values (?,?,?);"
            return self.sqlCommandParameterized(command, (ccpID, name, alliance))

    def insertPlayer(self, ccpID, name, corporation):
        command = "insert or ignore into players (ccpID, name, corporation) values (?,?,?);"
        return self.sqlCommandParameterized(command, (ccpID, name, corporation))

    def getSystemByCCPID(self, ccpID):
        command="select * from systems where ccpID=?;"
        return self.sqlCommandParameterized(command, (ccpID,))
    def getSystemByName(self, name):
        command="select * from systems where name = ?;"
        return self.sqlCommandParameterized(command, (ccpID,))
    def getCharacterByCCPID(self, ccpID):
        command = "select * from players where ccpID = ?;"
        return self.sqlCommandParameterized(command, (ccpID,))
    def getCharacterByName(self, name):
        command = "select * from players where name = ?;"
        return self.sqlCommandParameterized(command, (name,))
    
    def getCorpByCCPID(self, ccpID):
        command = "select * from corporations where ccpid = ?;"
        return self.sqlCommandParameterized(command, (ccpID,))
    def getCorpByName(self, name):
        command = "select* from corporations where name = ?;"
        return self.sqlCommandParameterized(command, (name,))
    def getAllianceByCCPID(self, ccpID):
        command = "select * from alliances where ccpid = ?;"
        return self.sqlCommandParameterized(command, (ccpID,))
    
    def getAllianceByName(self, name):
        command  = "select * from alliances where name = ?;"
        return self.sqlCommandParameterized(command, (name,))
    
    def getKillsByCharacterName(self, name):
        command ="select killmail from killsRaw km, kills k, attackers a, players p"
        command = command + " where p.name = ? and a.player = p.ID and a.kill = k.id and k.zKillID = km.zKillID"
        return self.sqlCommandParameterized(command, (name,))

    def getKillsByCharacterID(self, charID):
        command ="select killmail from killsRaw km, kills k, attackers a"
        command = command + " and a.player = ? and a.kill = k.id and k.zKillID = km.zKillID"
        return self.sqlCommandParameterized(command, (charID,))

    def getKillsWithMostAttackers(self,limit):
        command = ("""select count(a.id), k.zkillid from kills k, attackers a where a.kill = k.zkillid
                   group by k.zkillid  order by count(a.id) desc limit ?""")
        return self.sqlCommandParameterized(command, (limit,))


    def getKillsWithMostAttackersByCorp(self,limit, corpID):
        command = ("""select count(a.id), k.zkillid
                    from kills k, attackers a
                    where a.kill = k.zkillid
                     and ? in (
                         select corporation from attackers b
                         where b.kill = k.zkillid
                         )
                    group by k.zkillid
                   order by count(a.id) desc limit ?""")
        return self.sqlCommandParameterized(command, (corpID, limit,))


    def getKillsAndLossesByCorp(self, corpID):
        command = """select distinct k.zkillid, k.system, k.timeofdeath
                    from kills k inner join attackers a on a.kill=k.zkillid
                    where k.zkillid>0 and
                    (? =k.corporation or ?= a.corporation)
                    order by k.timeofdeath desc"""

        return self.sqlCommandParameterized(command, (corpID, corpID))

    def getKillsAndLossesByAlliance(self, allianceID):
        command = """select distinct k.zkillid, k.system, k.timeofdeath
                    from kills k inner join attackers a on a.kill=k.zkillid
                    where k.zkillid>0 and
                    (? =k.alliance or ?= a.alliance)
                    order by k.timeofdeath desc"""

        return self.sqlCommandParameterized(command, (allianceID, allianceID))


    def getKillsAndLossesByCharacter(self, charID):
        command = """select distinct k.zkillid, k.system, k.timeofdeath
                    from kills k inner join attackers a on a.kill=k.zkillid
                    where k.zkillid>0 and
                    (? =k.victim or ?= a.player)
                    order by k.timeofdeath desc"""

        return self.sqlCommandParameterized(command, (charID, charID))

    def getKillsAndLossesBySystem(self, system):
        command="""select distinct k.zkillid, k.victim, k.timeofdeath, k.corporation, k.alliance,  a.player, a.corporation, a.alliance
                    from kills k inner join attackers a on a.kill = k.zkillid
                    where k.zkillid>0 and k.system = ? order by k.timeofdeath desc;"""
        #pospy sol 31000510
        command="""

select aCorp, sum(aCorp2), max(timeofdeath), sum(daysrepresented), name 

from 

(select aCorp, count(aCorp)  as aCorp2, max(timeofdeath) as timeofdeath, count(distinct date(timeofdeath)) as daysRepresented, name
from (
			select k.zkillid, k.victim as kVic, k.corporation as vCorp, k.timeofdeath, k.corporation as kCorp, k.alliance as kAlliance,  a.player as aPlayer, a.corporation as aCorp, a.alliance as aAlliance 
		
                    from kills k inner join attackers a on a.kill = k.zkillid
                    where k.zkillid>0 and k.system = ?
					group by k.zkillid, aCorp, aAlliance
					order by k.timeofdeath desc
		), corporations
		where aCorp = corporations.ccpid
		group by  aCorp
		
		union 
		
		select vCorp, count(vCorp)  as vCorp2, max(timeofdeath) as timeofdeath, count(distinct date(timeofdeath)) as daysRepresented, name
			from (
			select k.zkillid, k.victim as kVic, k.corporation as vCorp, k.timeofdeath, k.corporation as kCorp, k.alliance as vAlliance, null,null,null
		
                    from kills k
                    where k.zkillid>0 and k.system = ?
					group by k.zkillid, vCorp, vAlliance
					order by k.timeofdeath desc
		), corporations
		where vCorp = corporations.ccpid
		group by  vCorp
		
		union
		
		select aAlliance, count(aAlliance) as aAlliance2, max(timeofdeath) as timeofdeath, count(distinct date(timeofdeath)) as daysRepresented, name
		from 
		(
		select k.zkillid, k.victim as kVic, k.corporation as vCorp, k.timeofdeath, k.corporation as kCorp, k.alliance as kAlliance,  a.player as aPlayer, a.corporation as aCorp, a.alliance as aAlliance 
		
                    from kills k inner join attackers a on a.kill = k.zkillid
                    where k.zkillid>0 and k.system = ?
					group by k.zkillid, aCorp, aAlliance
					order by k.timeofdeath desc
		
		), alliances 
		where aAlliance = alliances.ccpID
		group by aAlliance
		
		union 
		
		select vAlliance, count(vAlliance)  as vCorp2, max(timeofdeath) as timeofdeath, count(distinct date(timeofdeath)) as daysRepresented, name
			from (
			select k.zkillid, k.victim as kVic, k.corporation as vCorp, k.timeofdeath, k.corporation as kCorp, k.alliance as vAlliance, null,null,null
		
                    from kills k
                    where k.zkillid>0 and k.system = ?
					group by k.zkillid, vCorp, vAlliance
					order by k.timeofdeath desc
		), alliances
		where vAlliance = alliances.ccpID
		group by  vAlliance
		
		order by aCorp2 desc, timeofdeath
		
		
		) 
		group by aCorp
		order by aCorp2 desc, timeofdeath;
"""
        return self.sqlCommandParameterized(command, (system,system,system,system))

    def getEntityID(self, entity):

        array =["players", "corporations","alliances", "systems"]
        for i in array:
            command = "select ccpid from "+i+" where upper(name) = upper(?);"
            r = self.sqlCommandParameterized(command, (entity,))
            if(type(r) ==list and len(r) >0):
                return r[0][0]
        return None
        

##http://eve-search.com/thread/1336559-0#21
##
## return c1 pulsar
##"""SELECT invTypes.typeName, mapLocationWormholeClasses.wormholeClassID
##FROM eagle6_edb.mapDenormalize LEFT JOIN eagle6_edb.invTypes ON
##mapDenormalize.typeid = invTypes.typeID LEFT JOIN eagle6_edb.mapLocationWormholeClasses ON
##mapDenormalize.regionID = mapLocationWormholeClasses.locationID
##WHERE mapDenormalize.solarSystemID = '31000250' AND mapDenormalize.groupID = '995'"""    
