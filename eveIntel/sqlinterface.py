

import sqlite3 as sql
import sys
import os
from datetime import datetime

from eveIntel.sqlEngine import sqlEngine
from eveIntel.sqlEngineSqlite import sqlEngineSqlite
from eveIntel.sqlEnginePostgres import sqlEnginePostgres

class sqlConnection():
    #con = None
    def __init__(self):
        
        #default to sqlite
        #self.sqlEngine = sqlEngineSqlite()
        forcePostgres = sqlEnginePostgres()
        self.sqlEngine=forcePostgres
        
    def connect(self):
        return self.sqlEngine.connect()
    def commit(self):
        return self.sqlEngine.commit()
    def close(self):
        return self.sqlEngine.close()
        
    def setDBDir(self, d):
        return self.sqlEngine.setDBDir(d)
    def setConnection(self, connection):
        return self.setSqlEngine.setConnection(connection)
 

    def setSqlEngine(self, engine):
        if(not issubclass(type(engine), sqlEngine)):
            raise TypeError("engine:+" +str(type(engine))+" is not a subclass of sqlEngine")
        if(not (self.sqlEngine is None)):
            self.sqlEngine.close()
        self.sqlEngine = engine

    def __interactive(self):
        return self.sqlEngine.__interactive()


    def sqlCommand(self, command):
        return self.sqlEngine.sqlCommand(command)
        

    def sqlCommandParameterized(self, command, params):
        return self.sqlEngine.sqlCommandParameterized(command, params)

    def sqlCommandParameterizedWithoutCommit(self, command, params):
       
         return self.sqlEngine.sqlCommandParameterizedWithoutCommit(command, params)

    

    ##Inserts
    def insertRawKM(self, zkillID, rawKM, commit=False):
         return self.sqlEngine.insertRawKM( zkillID, rawKM, commit)
    
    def insertAlliance(self, ccpID, name, commit=False):
        return self.sqlEngine.insertAlliance(ccpID, name, commit)
    
    def insertCorp(self, ccpID, name, alliance=None, commit=False):
        return self.sqlEngine.insertCorp(ccpID, name, alliance, commit)
        

    def insertPlayer(self, ccpID, name, corporation, alliance=None, commit=False):
        return self.sqlEngine.insertPlayer(ccpID, name, corporation, alliance, commit)

    def insertAttacker(self, character, zkillID, damage, corpID, shipType, allianceID=None, commit=False):
        return self.sqlEngine.insertAttacker( character, zkillID, damage, corpID, shipType, allianceID, commit)

    def insertKill(self, zkill, victim, timeofdeath, system, corporation, ship, alliance=None, commit=False):
        return self.sqlEngine.insertKill( zkill, victim, timeofdeath, system, corporation, ship, alliance, commit)

    def insertSystem(self, ccpID, name, lastPulled='2003-01-01', commit=False):
        return self.sqlEngine.insertSystem( ccpID, name, lastPulled, commit)

    def setRawKillSkipped(self, killID, commit=False):
        return self.sqlEngine.setRawKillSkipped( killID, commit)

    def setRawKillProcessed(self, killID, commit=False):
        return self.sqlEngine.setRawKillProcessed( killID, commit)
    
    def invalidateReportCache(self):
        return self.sqlEngine.invalidateReportCache()


    ##Gets
    def getSystemByCCPID(self, ccpID):
        return self.sqlEngine.getSystemByCCPID( ccpID)
    def getSolarNameBySolarID(self, ccpID):
        return self.sqlEngine.getSolarNameBySolarID( ccpID)
    def getSystemByName(self, name):
        return self.sqlEngine.getSystemByName( name)
    def getCharacterByCCPID(self, ccpID):
        return self.sqlEngine.getCharacterByCCPID( ccpID)
    def getCharacterNameByCCPID(self, ccpID):
        return self.sqlEngine.getCharacterNameByCCPID( ccpID)
    def getCharacterByName(self, name):
        return self.sqlEngine.getCharacterByName(name)
    def getCharacterIDByName(self, name):
        return self.sqlEngine.getCharacterIDByName( name)

    
    def getCorpByCCPID(self, ccpID):
        return self.sqlEngine.getCorpByCCPID( ccpID)
    def getCorpByName(self, name):
        return self.sqlEngine.getCorpByName( name)
    def getAllianceByCCPID(self, ccpID):
        return self.sqlEngine.getAllianceByCCPID( ccpID)
    
    def getAllianceByName(self, name):
        return self.sqlEngine.getAllianceByName( name)
    def resetReportCache(self):
        return self.sqlEngine.resetReportCache()
    def getKillsByCharacterName(self, name):
        return self.sqlEngine.getKillsByCharacterName( name)

    def getKillsByCharacterID(self, charID):
        return self.sqlEngine.getKillsByCharacterID( charID)

    def getKillsWithMostAttackers(self, limit):
        return self.sqlEngine.getKillsWithMostAttackers(limit)


    def getKillsWithMostAttackersByCorp(self,limit, corpID):
        return self.sqlEngine.getKillsWithMostAttackersByCorp(limit, corpID)


    def getKillsAndLossesByCorp(self, corpID):
        return self.sqlEngine.getKillsAndLossesByCorp( corpID)

    def getKillsAndLossesByAlliance(self, allianceID):
        return self.sqlEngine.getKillsAndLossesByAlliance( allianceID)


    def getKillsAndLossesByCharacter(self, charID):
        return self.sqlEngine.getKillsAndLossesByCharacter( charID)

    def getKillsAndLossesBySystem(self, system):
        return self.sqlEngine.getKillsAndLossesBySystem( system)

    def getLeadershipByAlliance(self, allianceID):
        return self.sqlEngine.getLeadershipByAlliance( allianceID)
        
    def getLeadershipByCorp(self, corpID):
        return self.sqlEngine.getLeadershipByCorp( corpID)

    def getHrsByCorp(self, corpID):
        return self.sqlEngine.getHrsByCorp( corpID)

    def getHrsByAlliance(self, allianceID):
        return self.sqlEngine.getHrsByAlliance( allianceID)


    def getHrsByCharacter(self, charID):
        return self.sqlEngine.getHrsByCharacter( charID)

    def getSieges(self):
        return self.sqlEngine.getSieges()
    
    def getEntityID(self, entity):
        return self.sqlEngine.getEntityID( entity)
    
    def getCachedReport(self, reportType, entityID):
        return self.sqlEngine.getCachedReport(reportType, entityID)
    
    def insertCachedReport(self, reportType, entityID, content):
        return self.sqlEngine.insertCachedReport(reportType, entityID, content)

##http://eve-search.com/thread/1336559-0#21
##
## return c1 pulsar
##"""SELECT invTypes.typeName, mapLocationWormholeClasses.wormholeClassID
##FROM eagle6_edb.mapDenormalize LEFT JOIN eagle6_edb.invTypes ON
##mapDenormalize.typeid = invTypes.typeID LEFT JOIN eagle6_edb.mapLocationWormholeClasses ON
##mapDenormalize.regionID = mapLocationWormholeClasses.locationID
##WHERE mapDenormalize.solarSystemID = '31000250' AND mapDenormalize.groupID = '995'"""    

