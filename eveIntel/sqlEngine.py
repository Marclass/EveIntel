

from abc import ABCMeta, abstractmethod


class sqlEngine():
    
    __metaclass__ = ABCMeta

    def __init__(self):
        
        #self.dbDir = "D:\\sqlite3"
        self.dbDir = ""
        #os.chdir(self.dbDir)
        self.dbName = ""
        self.con = None
        
    
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def close(self):
        pass
        
    @abstractmethod
    def setDBDir(self, d):
        pass

    @abstractmethod
    def setConnection(self, connection):
        pass



    #@abstractmethod
    def __interactive(self):
        pass

    @abstractmethod
    def sqlCommand(self, command):
        pass
        
    @abstractmethod
    def sqlCommandParameterized(self, command, params):
        pass

    @abstractmethod
    def sqlCommandParameterizedWithoutCommit(self, command, params):
       pass

    

    ##Inserts
    @abstractmethod
    def insertRawKM(self, zkillID, rawKM, commit=False):
        pass
    
    @abstractmethod
    def insertAlliance(self, ccpID, name, commit=False):
        pass
    
    @abstractmethod
    def insertCorp(self, ccpID, name, alliance=None, commit=False):
        pass

    @abstractmethod
    def insertPlayer(self, ccpID, name, corporation, alliance=None, commit=False):
        pass
    
    @abstractmethod
    def insertAttacker(self, character, zkillID, damage, corpID, shipType, allianceID=None, commit=False):
        pass

    @abstractmethod
    def insertKill(self, zkill, victim, timeofdeath, system, corporation, ship, alliance=None, commit=False):
        pass
    
    @abstractmethod
    def insertSystem(self, ccpID, name, lastPulled='2003-01-01', commit=False):
        pass
    @abstractmethod
    def setRawKillSkipped(self, killID, commit=False):
        pass
    @abstractmethod
    def setRawKillProcessed(self, killID, commit=False):
        pass
    @abstractmethod
    def invalidateReportCache(self):
        pass


    ##Gets
    @abstractmethod
    def getSystemByCCPID(self, ccpID):
        pass
    @abstractmethod
    def getSolarNameBySolarID(self, ccpID):
        pass
    @abstractmethod
    def getSystemByName(self, name):
        pass
    @abstractmethod
    def getCharacterByCCPID(self, ccpID):
        pass
    @abstractmethod
    def getCharacterNameByCCPID(self, ccpID):
        pass
    @abstractmethod
    def getCharacterByName(self, name):
        pass
    @abstractmethod
    def getCharacterIDByName(self, name):
        pass

    @abstractmethod
    def getCorpByCCPID(self, ccpID):
        pass
    @abstractmethod
    def getCorpByName(self, name):
        pass
    @abstractmethod
    def getAllianceByCCPID(self, ccpID):
        pass
    
    def getAllianceByName(self, name):
        pass
    @abstractmethod
    def resetReportCache(self):
        pass
    @abstractmethod
    def getKillsByCharacterName(self, name):
        pass
    @abstractmethod
    def getKillsByCharacterID(self, charID):
        pass
    @abstractmethod
    def getKillsWithMostAttackers(self,limit):
        pass

    @abstractmethod
    def getKillsWithMostAttackersByCorp(self,limit, corpID):
        pass

    @abstractmethod
    def getKillsAndLossesByCorp(self, corpID):
        pass
    @abstractmethod
    def getKillsAndLossesByAlliance(self, allianceID):
        pass

    @abstractmethod
    def getKillsAndLossesByCharacter(self, charID):
        pass
    @abstractmethod
    def getKillsAndLossesBySystem(self, system):
        pass
    @abstractmethod
    def getLeadershipByAlliance(self, allianceID):
        pass

    @abstractmethod
    def getLeadershipByCorp(self, corpID):
        pass

    @abstractmethod
    def getHrsByCorp(self, corpID):
        pass

    @abstractmethod
    def getHrsByAlliance(self, allianceID):
        pass

    @abstractmethod
    def getHrsByCharacter(self, charID):
        pass

    @abstractmethod
    def getSieges(self):
        pass
    
    @abstractmethod
    def getEntityID(self, entity):
        pass
    
    @abstractmethod
    def getCachedReport(self, reportType, entityID):
        pass
    
    @abstractmethod
    def insertCachedReport(self, reportType, entityID, content):
        pass

#sqlEngine.register(sqlEngineSqlite)

