
from EveCommon.ZKillboard import ZKillboard
from evelinkinterface import *
from datetime import datetime, timedelta
from eveIntel.sdeinterface import sdeInterface



class zKillInterface():
    sde = sdeInterface()
    ec_useragent="EveIntel Default UserAgent/ Can not read directions"



    def getKillsInSystemBySystemName(self, system ):
        #end = datetime.now()
        #lastXsec = 60*60*24*7
        #start = end - timedelta(days=7)
        solID = self.sde.getSolarIDBySolarName(system)

        zKill = ZKillboard(user_agent = self.ec_useragent, losses = True, solar_system_id= solID)

        killmails = zKill.get_killmails()
        return killmails


    def getKillsInSystemBySystemID(self, solID, start = None):
        #end = datetime.now()
        #lastXsec = 60*60*24*7
        #start = end - timedelta(days=7)
        #solID = self.sde.getSolarIDBySolarName(system)
        if(start is None):
            zKill = ZKillboard(user_agent = self.ec_useragent, losses = True, solar_system_id= solID)
        else:
            zKill = ZKillboard(user_agent = self.ec_useragent, losses = True, solar_system_id= solID, start_time = start)

            
        killmails = zKill.get_killmails()
        return killmails

    
    def getKillsOfCorpByCorpName(self, corpName):
        #end = datetime.now()
        #start = end - lastXSec
        #solID = sde.getSolarIDBySolarName(system)

        link = evelinkinterface()
        corpID = link.resolveIDFromName(corpName)

        zKill = ZKillboard(user_agent = self.ec_useragent, losses = True, no_attackers=True, corporation_id = corpID)

        killmails = zKill.get_killmails()
        return killmails

    def getWSpaceKillsOfCorpByCorpName(self, corpName):
        link = evelinkinterface()
        corpID = link.resolveIDFromName(corpName)

        return self.getWSpaceKillsOfCorpByCorpID(corpID)

    def getWSpaceKillsOfCorpByCorpID(self, corpID):
        #end = datetime.now()
        #start = end - lastXSec
        #solID = sde.getSolarIDBySolarName(system)

        #link = evelinkinterface()
        #corpID = link.resolveIDFromName(corpName)

        zKill = ZKillboard(user_agent = self.ec_useragent, losses = False, corporation_id = corpID, wspace =True)

        killmails = zKill.get_killmails()
        return killmails


    def getWSpaceLossesOfCorpByCorpName(self, corpName):
        link = evelinkinterface()
        corpID = link.resolveIDFromName(corpName)

        return self.getWSpaceLossesOfCorpByCorpID(corpID)


    def getWSpaceLossesOfCorpByCorpID(self, corpID):

        zKill = ZKillboard(user_agent = self.ec_useragent, losses = True, corporation_id = corpID, wspace =True)

        killmails = zKill.get_killmails()
        return killmails
        
    def sortKillsBySystem(self, kills):
        #should really move this to a data processing class but w/e
        from operator import itemgetter
        #returns (systemID, number of Kills) tuple
        whSystems={}
        for i in range(len(kills)):
            sol=str(kills[i].solarSystemID)
            if(sol in whSystems):
                whSystems[sol] = whSystems[sol]+1
            else:
                whSystems[sol] = 1
        sortedWH = sorted(whSystems.items(), key = itemgetter(1), reverse = True)

        
        return sortedWH

    def testImportFunction(commnet):
        print(comment)


    def testPrintKillList(self, killList, outFile):
        out= open(outFile, "w")
        for kill in killList:
            out.write(str(kill.__dict__)+"\n")
        out.flush()
        out.close()

    def readTestPrintKills(self, inFile):
        import ast
        
        killFile = open(inFile, "r")
        kills =[]
        for line in killFile.readlines():
            kills.append(ast.literal_eval(line))
        killFile.close()
        return kills
            


    if(False):
        corpName = "Pos Party"
        corpName ="Alfa s Centavry"
        systemName="J152654"
        systemTest = ""#getKillsInSystemBySystemName(systemName)
        corpTest = ""#getWSpaceKillsOfCorpByCorpName(corpName)

        link = evelinkinterface()

        x= link.resolveIDFromName(corpName)
        print("system kill num= "+len(systemTest))
        print("corp kill num= "+len(corpTest))
        print(x)
