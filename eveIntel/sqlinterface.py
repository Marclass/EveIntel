

import sqlite3 as sql
import sys
import os
from datetime import datetime


class sqlConnection():
    #con = None
    def __init__(self):
        
        #self.dbDir = "D:\\sqlite3"
        self.dbDir = "I:\\sqlite3"
        os.chdir(self.dbDir)
        self.dbName = "test.db"
        self.con = None
        self.dedicatedCursor=None
        
    def connect(self):
        self.con = sql.connect(self.dbName, check_same_thread=False)
    def commit(self):
        self.con.commit()
    def close(self):
        self.con.close()
        
    def setDBDir(self, d):
        self.dbDir = d
    def setConnection(self, connection):
        print("connection set")
        if(self.con):
            self.con.close()
            print("closed connection")
        self.con = connection
    def setDedicatedCursor(self, cur):
        self.dedicatedCursor=cur 

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
    def sqlCommandParameterizedWithoutCommit(self, command, params):
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

    

    ##Inserts
    def insertRawKM(self, zkillID, rawKM, commit=False):
        f=self.sqlCommandParameterized
        if(commit):
            f=self.sqlCommandParameterizedWithoutCommit

        
        command="insert or ignore into killsRaw (zKillID, killmail, processed, skipped) values (?,?, 'False','False');"
        return f(command, (zkillID, rawKM))

    def insertAlliance(self, ccpID, name, commit=False):
        f=self.sqlCommandParameterized
        if(commit):
            f=self.sqlCommandParameterizedWithoutCommit

        command = "insert or ignore into alliances (ccpID, name) values (?,?);"
        return f(command, (ccpID, name))
    
    def insertCorp(self, ccpID, name, alliance=None, commit=False):
        f=self.sqlCommandParameterized
        if(commit):
            f=self.sqlCommandParameterizedWithoutCommit

        if(alliance is None):
            command = "insert or ignore into corporations (ccpID, name) values (?,?);"
            return f(command, (ccpID, name)) 
        else:
            command = "insert or ignore into corporations (ccpID, name, alliance) values (?,?,?);"
            return f(command, (ccpID, name, alliance))

    def insertPlayer(self, ccpID, name, corporation, alliance=None, commit=False):
        f=self.sqlCommandParameterized
        if(commit):
            f=self.sqlCommandParameterizedWithoutCommit

        if(alliance is None):
            command = "insert or ignore into players (ccpID, name, corporation) values (?,?,?);"
            return f(command, (ccpID, name, corporation))
        else:
            command="insert or ignore into players (ccpID, name, corporation, alliance) values (?,?,?,?);"
            return f(command, (ccpID, name, corporation, alliance))

    def insertAttacker(self, character, zkillID, damage, corpID, shipType, allianceID=None, commit=False):
        command=""
        f=self.sqlCommandParameterized
        if(commit):
            f=self.sqlCommandParameterizedWithoutCommit

        if(allianceID is None):
            command="insert or replace into attackers (player, kill, damage, corporation, ship) values (?,?,?,?,?);"
            return f(command, (character, zkillID, damage, corpID, shipType))
        else:
            command="insert or replace into attackers (player, kill, damage, corporation, alliance, ship) values (?,?,?,?,?,?);"
            return f(command, (character, zkillID, damage, corpID, allianceID, shipType))

    def insertKill(self, zkill, victim, timeofdeath, system, corporation, ship, alliance=None, commit=False):
        command=""
        f=self.sqlCommandParameterized
        if(commit):
            f=self.sqlCommandParameterizedWithoutCommit

        if(alliance is None):
            command="insert or ignore into kills (zKillID, victim, timeOfDeath, system, corporation, ship) values (?,?,?,?,?,?);"
            return f(command, (zkill, victim, timeofdeath, system, corporation, ship))
        else:
            command="insert or ignore into kills (zKillID, victim, timeOfDeath, system, corporation, alliance, ship) values (?,?,?,?,?,?,?);"
            return f(command, (zkill, victim, timeofdeath, system, corporation, alliance, ship))

    def insertSystem(self, ccpID, name, lastPulled='2003-01-01', commit=False):
        command="insert or ignore into systems (ccpid, name, lastPulled) values (?,?, date(?));"
        f=self.sqlCommandParameterized
        if(commit):
            f=self.sqlCommandParameterizedWithoutCommit

        return f(command, (ccpID, name, str(lastPulled)))

    def setRawKillSkipped(self, killID, commit=False):
        command = "update killsraw set skipped ='True' where id=?"
        f=self.sqlCommandParameterized
        if(commit):
            f=self.sqlCommandParameterizedWithoutCommit
        return f(command, (killID,))

    def setRawKillProcessed(self, killID, commit=False):
        command = "update killsraw set processed ='True' where id=?"
        f=self.sqlCommandParameterized
        if(commit):
            f=self.sqlCommandParameterizedWithoutCommit
        return f(command, (killID,))
    
    def invalidateReportCache(self):
        return self.sqlCommand("update reportCache set valid ='False';")


    ##Gets
    def getSystemByCCPID(self, ccpID):
        command="select * from systems where ccpID=?;"
        return self.sqlCommandParameterized(command, (ccpID,))
    def getSolarNameBySolarID(self, ccpID):
        command="select name from systems where ccpid=?;"
        return self.sqlCommandParameterized(command, (ccpID,))
    def getSystemByName(self, name):
        command="select * from systems where name = ?;"
        return self.sqlCommandParameterized(command, (ccpID,))
    def getCharacterByCCPID(self, ccpID):
        command = "select * from players where ccpID = ?;"
        return self.sqlCommandParameterized(command, (ccpID,))
    def getCharacterNameByCCPID(self, ccpID):
        command = "select name from players where ccpID = ?;"
        return self.sqlCommandParameterized(command, (ccpID,))
    def getCharacterByName(self, name):
        command = "select * from players where name = ?;"
        return self.sqlCommandParameterized(command, (name,))
    def getCharacterIDByName(self, name):
        command = "select ccpid from players where name = ?;"
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
    def resetReportCache(self):
        command ="update reportcache set valid='False'"
        return self.sqlCommand(command)
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

    def getLeadershipByAlliance(self, allianceID):
        command="""
select player, p.name, sum(killCount) as killCount2, sum(totalKillCount) as totalKillCount2, (sum(killCount)+0.0)/sum(totalKillCount) as fightPercent2, count(player) as fightNum

from 
(select player, killCount, system, tod, totalKillCount

from (select * from 
(select player, count(distinct kill) as killCount , system, date(timeofdeath) as tod

from 	
	(select a1.kill, a1.player, k1.system, k1.timeofdeath 
	from attackers a1, kills k1 
	where 
		a1.alliance=? and 
		(select count(1) from attackers where kill = a1.kill)>=5 and 
		a1.kill = k1.zkillid and 
		a1.alliance = (select a2.alliance from attackers a2 where a1.player = a2.player order by kill desc limit 1)
		and date(k1.timeofdeath) >= date('now', '-6 month') 
		) kp 
		
		group by player, system, date(timeofdeath) ) s1
		--group by system, date(timeofdeath)
inner join 		

(select system, date(timeofdeath) as tod, count(distinct kill) as totalkillCount 

from 	
	(select a1.kill, a1.player, k1.system, k1.timeofdeath 
	from attackers a1, kills k1 
	where 
		a1.alliance=? and 
		(select count(1) from attackers where kill = a1.kill)>=5 and 
		a1.kill = k1.zkillid and 
		a1.alliance = (select a2.alliance from attackers a2 where a1.player = a2.player order by kill desc limit 1)
		and date(k1.timeofdeath) >= date('now', '-6 month') 
		) kp 
		
		group by system, date(timeofdeath) ) s2
		 
		on s1.system =s2.system and s1.tod = s2.tod
		)
		), players p where player = p.ccpid 
		
		group by player
		order by fightNum desc;
"""
        return self.sqlCommandParameterized(command, (allianceID, allianceID))
        
    def getLeadershipByCorp(self, corpID):
        command="""
select player, p.name, sum(killCount) as killCount2, sum(totalKillCount) as totalKillCount2, (sum(killCount)+0.0)/sum(totalKillCount) as fightPercent2, count(player) as fightNum

from 
(select player, killCount, system, tod, totalKillCount

from (select * from 
(select player, count(distinct kill) as killCount , system, date(timeofdeath) as tod

from 	
	(select a1.kill, a1.player, k1.system, k1.timeofdeath 
	from attackers a1, kills k1 
	where 
		a1.corporation=? and 
		(select count(1) from attackers where kill = a1.kill)>=5 and 
		a1.kill = k1.zkillid and 
		a1.corporation = (select a2.corporation from attackers a2 where a1.player = a2.player order by kill desc limit 1)
		and date(k1.timeofdeath) >= date('now', '-6 month') 
		) kp 
		
		group by player, system, date(timeofdeath) ) s1
		--group by system, date(timeofdeath)
inner join 		

(select system, date(timeofdeath) as tod, count(distinct kill) as totalkillCount 

from 	
	(select a1.kill, a1.player, k1.system, k1.timeofdeath 
	from attackers a1, kills k1 
	where 
		a1.corporation=? and 
		(select count(1) from attackers where kill = a1.kill)>=5 and 
		a1.kill = k1.zkillid and 
		a1.corporation = (select a2.corporation from attackers a2 where a1.player = a2.player order by kill desc limit 1)
		and date(k1.timeofdeath) >= date('now', '-6 month') 
		) kp 
		
		group by system, date(timeofdeath) ) s2
		 
		on s1.system =s2.system and s1.tod = s2.tod
		)
		), players p where player = p.ccpid 
		
		group by player
		order by fightNum desc;
"""
        return self.sqlCommandParameterized(command, (corpID, corpID))

    def getHrsByCorp(self, corpID):
        command="""select substr(time(ks.timeofdeath),0,3)||':00' as hr, count(distinct ks.zkillid) 
from kills ks where ks.zkillid in
(
select distinct k.zkillid as zkillid
from kills k 
where k.corporation = ?

union 

select distinct a.kill
from attackers a
where a.corporation = ?) 

group by hr"""
        return self.sqlCommandParameterized(command, (corpID, corpID))

    def getHrsByAlliance(self, allianceID):
        command="""select substr(time(ks.timeofdeath),0,3)||':00' as hr, count(distinct ks.zkillid) 
from kills ks where ks.zkillid in
(
select distinct k.zkillid as zkillid
from kills k 
where k.alliance = ?

union 

select distinct a.kill
from attackers a
where a.alliance = ?) 

group by hr"""
        return self.sqlCommandParameterized(command, (allianceID, allianceID))


    def getHrsByCharacter(self, charID):
        command="""select substr(time(ks.timeofdeath),0,3)||':00' as hr, count(distinct ks.zkillid) 
from kills ks where ks.zkillid in
(
select distinct k.zkillid as zkillid
from kills k 
where k.victim = ?

union 

select distinct a.kill
from attackers a
where a.player = ?) 

group by hr"""
        return self.sqlCommandParameterized(command, (charID, charID))

    def getSieges(self):
        command="""select s.name as systemName, c1.name as siegedCorpName, date(k.timeofdeath) as timeofdeath, c2.name as siegingCorpName, count(distinct k.zkillid) as numDeaths, count(distinct a.player) as numAttackers
from
kills k, attackers a, corporations  as c1, corporations  as c2, systems s

where k.zkillID in (select k.zkillid from kills k where victim = 0 and k.ship != 33475 and k.ship !=33474 and date(timeofdeath)>= date('now', '-2 day'))
and k.corporation = c1.ccpid and k.zkillid = a.kill and a.corporation = c2.ccpid and k.system = s.ccpid

group by system, siegedCorpName, date(timeofdeath)

order by numDeaths desc limit 15"""
        return self.sqlCommand(command)
    
    def getEntityID(self, entity):

        array =["players", "corporations","alliances", "systems"]
        for i in array:
            command = "select ccpid from "+i+" where upper(name) = upper(?);"
            r = self.sqlCommandParameterized(command, (entity,))
            if(type(r) ==list and len(r) >0):
                return r[0][0]
        return None
    
    def getCachedReport(self, reportType, entityID):
        command="""select content from reportCache
where reportType=? and entityID =? and valid='True';"""
        return self.sqlCommandParameterized(command, (reportType, entityID))
    
    def insertCachedReport(self, reportType, entityID, content):
        command="""insert or replace into
reportCache(reportType, entityID, cacheTime, content, valid)
values(?,?,?,?,'True');"""
        dateTime = str(datetime.now())
        self.sqlCommandParameterized(command, (reportType, entityID, dateTime, content))

##http://eve-search.com/thread/1336559-0#21
##
## return c1 pulsar
##"""SELECT invTypes.typeName, mapLocationWormholeClasses.wormholeClassID
##FROM eagle6_edb.mapDenormalize LEFT JOIN eagle6_edb.invTypes ON
##mapDenormalize.typeid = invTypes.typeID LEFT JOIN eagle6_edb.mapLocationWormholeClasses ON
##mapDenormalize.regionID = mapLocationWormholeClasses.locationID
##WHERE mapDenormalize.solarSystemID = '31000250' AND mapDenormalize.groupID = '995'"""    

