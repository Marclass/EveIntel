from eveIntel.evelinkinterface import evelinkinterface
from eveIntel.sqlinterface import sqlConnection
from tabulate import tabulate
from eveIntel.sdeinterface import sdeInterface
from eveIntel.Exceptions import *


from ascii_graph import Pyasciigraph

import time
from datetime import date
import datetime
from ast import literal_eval
import inspect
#Characters: ]90000000, 98000000[ ## only applies to stuff made after 64 bit
#Corporations: ]98000000, 99000000[ ## move, older shit will not fall in
#Alliances: ]99000000, 100000000[## these ranges :(
class dataProcessingInterface():
    def __init__(self):
        self.eve  = evelinkinterface()
        self.sql = sqlConnection()
        self.sql.connect()
        #self.sql.resetReportCache()
        self.sde = sdeInterface()

        self.homeHeader=["System", "#Kills", "#Losses", "Kill dt avg",
                "Loss dt avg", "Kill dt variance", "Loss dt variance",
                "First Kill/Loss", "Last Kill/Loss", "Certainty"]

        
    def genericReportWithErrorHandeling(self, validationReportPairs, args):
        """attempts to run given reports and returns value for first report that passes input validation
        want to use to reduce redundant code for starting different reports
        return report value or None on failure"""
        self.isDBlocked()
        for i in validationReportPairs:
            validator = i[0]
            report = i[1]
            start = int(time.time())
            if(validator(args)):
                end = int(time.time())
                print(str(validator.func_name) +" took: "+str(end-start))
                #print(report)
                print(str(report.func_name)+" report at "+str(datetime.datetime.now()))
                return report(args)
        return None


    def genReport(self, entity):
        """more compact genReport"""
        print("generating home/Sol report for: "+str(entity))
        pairs=[]
        pairs.append((self.isChar, self.genCharReport))
        pairs.append((self.isCorp, self.genCorpReport))
        pairs.append((self.isAlliance, self.genAllianceReport))
        pairs.append((self.isSystem, self.genSolReport))
        
        entityID = self.sql.getEntityID(entity)
        if(entityID is None):
            self.entityNotFound(entity)
            
        report = self.genericReportWithErrorHandeling(pairs, entityID)

        if(report is None):
            self.entityNotFound(entity)
        return report
        

    def genReportRaw(self, entity):
        report = ""
        start = int(time.time())
        entityID = self.sql.getEntityID(entity)
        end = int(time.time())

        print("it took "+ str(end-start) +" seconds to look up: "+ str(entity))
        
        #if(entityID is None):
            #entityID = self.eve.resolveIDFromName(entity)
        #print(entityID)
        if(not isinstance(entityID, int)):
            lastTOD = self.sql.sqlCommand("select max(timeofdeath) from kills")
            if(lastTOD is None):
                return "The DB appears to be locked. The previous day's kills are likely being processed, please wait a few minutes and try again."
            if(len(lastTOD)>0):
                lastTOD=lastTOD[0][0]
            else:
                return "The DB appears to be locked. The previous day's kills are likely being processed, please wait a few minutes and try again."
            return "Entity: \""+ str(entity) +"\" has no kill/death history in w space as of "+str(lastTOD)
        start = int(time.time())
        if(self.isChar(entityID)):
            end  = int(time.time())
            print("isX took: "+str(end-start)+"")
            return self.genCharReportRaw(entityID)
        elif(self.isCorp(entityID)):
            end  = int(time.time())
            print("isX took: "+str(end-start)+"")
            return self.genCorpReportRaw(entityID)
        elif(self.isAlliance(entityID)):
            end  = int(time.time())
            print("isX took: "+str(end-start)+"")
            return self.genAllianceReportRaw(entityID)
        elif(self.isSystem(entityID)):
            end  = int(time.time())
            print("isX took: "+str(end-start)+"")
            return self.genSolReportRaw(entityID)
        else:
            lastTOD = self.sql.sqlCommand("select max(timeofdeath) from kills")

            if(len(lastTOD)>0):
                lastTOD=lastTOD[0][0]
            else:
                return "The DB appears to be locked. The previous day's kills are likely being processed, please wait a few minutes and try again."
            
            return "Entity: \""+ str(entity) +"\" has no kill/death history in w space as of "+str(lastTOD)
        return report
    

    def isChar(self, entityID):
        if(int(entityID)>=90000000 and (int(entityID) <98000000)):
            return True
        #print("isChar checking db")
        return len(self.sql.getCharacterByCCPID(entityID)) >0
        #return False

    def isCorp(self, entityID):
        if(int(entityID)>=98000000 and (int(entityID) <99000000)):
            return True
        return len(self.sql.getCorpByCCPID(entityID)) >0
        
        #return False
        
    def isAlliance(self, entityID):
        if(int(entityID)>=99000000 and (int(entityID) <100000000)):
            return True
        return len(self.sql.getAllianceByCCPID(entityID)) >0

        #return False
    def isSystem(self, entityID):
        if(entityID==31000005 or (entityID >=31000007 and entityID <= 31002605)):
            return True
        return False

    def genCharReport(self, char):
        key = "characterID"
        
        #kills = self.sql.getKillsByCharacterID(char)
        #losses = self.sql.getLossesByCharacterID(char)

        start = int(time.time())
        
        r=self.sql.getCachedReport(self.getHomeReportType(), char)
        if(len(r)>0):
            print("using cache")
            end = int(time.time())

            print("elapsed time was "+str(end-start) +" seconds to pull kills for corp: "+str(char))
            return self.findCharHome(char, key, [],[])
        
        report =""
        
        kills = self.sql.getKillsAndLossesByCharacter(char)
        #print(type(kills))
        #print(kills)
        end = int(time.time())
        print("elapsed time was "+str(end-start) +" seconds to pull kills for corp: "+str(char))
        
        if(type(kills) == str):
            return kills
        home = self.findCharHome(char, key, kills, [])
        report = home
        return report

    def genCharReportRaw(self, char):
        key = "characterID"
        
        #kills = self.sql.getKillsByCharacterID(char)
        #losses = self.sql.getLossesByCharacterID(char)
        
        start = int(time.time())

        r=self.sql.getCachedReport(self.getHomeReportType(), char)
        if(len(r)>0):
            print("using cache")
            end = int(time.time())

            print("elapsed time was "+str(end-start) +" seconds to pull kills for corp: "+str(char))
            return self.findCharHomeRaw(char, key, [],[])
        
        report =""
        
        kills = self.sql.getKillsAndLossesByCharacter(char)
        #print(type(kills))
        #print(kills)

        end = int(time.time())

        print("elapsed time was "+str(end - start) +" seconds to pull kills for corp: "+str(char))
        
        if(type(kills) == str):
            return kills
        home = self.findCharHomeRaw(char, key, kills, [])
        report = home
        return report


    def genCorpReport(self, corp):
        key = "corporationID"
        report =""
        start = int(time.time())

        r=self.sql.getCachedReport(self.getHomeReportType(), corp)
        if(len(r)>0):
            print("using cache")
            end = int(time.time())

            print("elapsed time was "+str(end-start) +" seconds to pull kills for corp: "+str(corp))
            return self.findCharHome(corp, key, [],[])
        
        kills = self.sql.getKillsAndLossesByCorp(corp)

        end = int(time.time())

        print("elapsed time was "+str(end-start) +" seconds to pull kills for corp: "+str(corp))
        if(type(kills) == str):
            return kills

        start = int(time.time())
        
        home = self.findCharHome(corp, key, kills, [])
        end = int(time.time())

        print("elapsed time was "+str(end-start) +" seconds to process kills for corp: "+str(corp))
        
        report = home
        return report

    def genCorpReportRaw(self, corp):
        key = "corporationID"
        report =""
        start = int(time.time())

        r=self.sql.getCachedReport(self.getHomeReportType(), corp)
        if(len(r)>0):
            print("using cache")
            end = int(time.time())

            print("elapsed time was "+str(end-start) +" seconds to pull kills for corp: "+str(corp))
            return self.findCharHomeRaw(corp, key, [],[])
        
        kills = self.sql.getKillsAndLossesByCorp(corp)

        end = int(time.time())

        print("elapsed time was "+str(end-start) +" seconds to pull kills for corp: "+str(corp))
        if(type(kills) == str):
            return kills

        start = int(time.time())
        
        home = self.findCharHomeRaw(corp, key, kills, [])
        end = int(time.time())

        print("elapsed time was "+str(end-start) +" seconds to process kills for corp: "+str(corp))
        
        report = home
        
        return report

    def genAllianceReport(self, alliance):
        key = "allianceID"
        report =""

        start = int(time.time())

        r=self.sql.getCachedReport(self.getHomeReportType(), alliance)
        if(len(r)>0):
            print("using cache")
            end = int(time.time())

            print("elapsed time was "+str(end-start) +" seconds to pull kills for corp: "+str(alliance))
            return self.findCharHome(alliance, key, [],[])
        
        kills = self.sql.getKillsAndLossesByAlliance(alliance)

        end = int(time.time())

        print("elapsed time was "+str(end-start) +" seconds to pull kills for corp: "+str(alliance))
        
        if(type(kills) == str):
            return kills
        
        home = self.findCharHome(alliance, key, kills, [])
        report = home
        return report

    def genAllianceReportRaw(self, alliance):
        key = "allianceID"
        report =""

        start = int(time.time())

        r=self.sql.getCachedReport(self.getHomeReportType(), alliance)
        if(len(r)>0):
            print("using cache")
            end = int(time.time())

            print("elapsed time was "+str(end-start) +" seconds to pull kills for corp: "+str(alliance))
            return self.findCharHomeRaw(alliance, key, [],[])
        
        kills = self.sql.getKillsAndLossesByAlliance(alliance)

        end = int(time.time())

        print("elapsed time was "+str(end-start) +" seconds to pull kills for corp: "+str(alliance))
        
        if(type(kills) == str):
            return kills
        
        home = self.findCharHomeRaw(alliance, key, kills, [])
        report = home
        return report


    def genLeadershipReport(self, entity):
        #genericReportWithErrorHandeling
        print("gnerating leadership report for: "+str(entity))
        pairs=[]
        pairs.append((self.isChar, self.charLeadershipReportFailureWrapper))
        pairs.append((self.isCorp, self.genCorpLeadershipReport))
        pairs.append((self.isAlliance, self.genAllianceLeadershipReport))

        entityID = self.sql.getEntityID(entity)
        if(entityID is None):
            self.entityNotFound(entity)
            
        report = self.genericReportWithErrorHandeling(pairs, entityID)

        if(report is None):
            self.entityNotFound(entity)
        return report

    
    def charLeadershipReportFailureWrapper(self, entity):
        entity = self.sql.getCharacterNameByCCPID(entity)[0][0]
        return self.invalidInputMsg(entity, "LeadershipReport")

    
    def genSiegeReport(self):
        print("generating siege report")

        r=self.sql.getCachedReport(self.getSiegeReportType(), 0)
        if(len(r)>0 and False):
            print("using cache")
            rows = literal_eval(r[0][0])
            
            return tabulate(rows, headers = rhead)
            
            
        sieges = self.sql.getSieges()
        rhead = ["System", "Besieged", "Siege Date", "Siegers", "num Structures killed", "num Attackers"]

        rows=[]
        for i in sieges:
            rows.append( (i[0],i[1],i[2],i[3],i[4], i[5]) )

        self.sql.insertCachedReport(self.getSiegeReportType(), 0, str(rows))
        response = tabulate(rows, headers = rhead)

        return response
    
    def genCorpLeadershipReport(self, corpID):

        start = int(time.time())
        
        r = self.genEntityLeadershipReport(self.sql.getLeadershipByCorp, corpID) 

        end = int(time.time())

        print("elapsed time was "+str(end-start) +" seconds to gen leadership for corp: "+str(corpID))
        
        return r
        
        

    def genAllianceLeadershipReport(self, allianceID):

        start = int(time.time())
        
        r = self.genEntityLeadershipReport(self.sql.getLeadershipByAlliance, allianceID)

        end = int(time.time())

        print("elapsed time was "+str(end-start) +" seconds to gen leadership for alliance: "+str(allianceID))
        
        return r
    


    def genEntityLeadershipReport(self, sqlCall, eID):
        rhead=["Pilot", "KillCount", "PossibleKills", "Whore %", "NumFights", "Confidence"]
        
        r=self.sql.getCachedReport(self.getLeadershipReportType(), eID)
        if(len(r)>0):
            print("using cache")
            rows = literal_eval(r[0][0])
            #print(rows)
            #print(r)
            return tabulate(rows, headers = rhead)
            #rows=[]
        
        rtable=""
        players = sqlCall(eID)
        
        sort = self.processLeadershipReport(players)
        rows=[]
        for i in sort:
            rows.append((i[1],i[2],i[3],i[4],i[5],i[6]))
        if(len(rows)==0):
            raise DBLockedException()
        
        self.sql.insertCachedReport(self.getLeadershipReportType(), eID, str(rows))
        #print(str(type(rows) )+"\n"+str(rows))
        response = tabulate(rows, headers = rhead)

        return response

    def processLeadershipReport(self, rows):
        l=[]

        for i in rows:
            #calc confidence and append it to row then sort by confidence
            killCount = i[2]
            totalKills = i[3]
            fightPercent =i[4]
            fightNum = i[5]
            #print(i)
            
            confidence = fightPercent**2 * 2**(fightNum/3)

            l.append(list(i))
            
            l[-1].append(confidence)

        l.sort(key = lambda x:x[-1], reverse = True)

        return l[:15]

    def genHrsReport(self, entity):
        #genericReportWithErrorHandeling
        print("generating hrs report for: "+str(entity))
        pairs=[]
        
        pairs.append((self.isChar, self.genCharacterHrsReport))
        pairs.append((self.isCorp, self.genCorpHrsReport))
        pairs.append((self.isAlliance, self.genAllianceHrsReport))


        entityID = self.sql.getEntityID(entity)
        if(entityID is None):
            self.entityNotFound(entity)
            
        report = self.genericReportWithErrorHandeling(pairs, entityID)

        if(report is None):
            self.entityNotFound(entity)
        return report

    
   
    def genEntityHrsReport(self, hrFunction, eID):

        r=self.sql.getCachedReport(self.getHrsReportType(), eID)
        if(len(r)>0):
            print("using cache")
            rows = literal_eval(r[0][0])
        else:
            rows = hrFunction(eID)
        #print(rows)
        self.sql.insertCachedReport(self.getHrsReportType(), eID, str(rows))
        
        graph = Pyasciigraph()
        ascii = ""
        for line in graph.graph('Activity by time of day (Eve time)', rows):
            ascii = ascii+line+"\n"
        return ascii

    def genCorpHrsReport(self, corpID):
        return self.genEntityHrsReport(self.sql.getHrsByCorp, corpID)
    def genAllianceHrsReport(self, allianceID):
        return self.genEntityHrsReport(self.sql.getHrsByAlliance, allianceID)
    def genCharacterHrsReport(self, charID):
        return self.genEntityHrsReport(self.sql.getHrsByCharacter, charID)
        
    def genSolReport(self, sol, useCache=True):
        #print("start genSolReport")
        rhead =["corporation", "Kills+losses", "Days Represented","Confidence Rating", "Most recent kill/loss"]

        rows = self.genSolReportRaw(sol)
        #print(len(rows))
        response = tabulate(rows, headers = rhead)

        
        return response

    def genSolReportRaw(self, sol):
        key = "solarSystemID"
        
        r=self.sql.getCachedReport(self.getSolReportType(), sol)
        if(len(r)>0):
            print("using cache")
            return literal_eval(r[0][0])

        kills = self.sql.getKillsAndLossesBySystem(sol)
        #print("kills Len= "+str(len(kills)))
        mails = self.processSolReportKills(kills)
        rhead =["corporation", "Kills+losses", "Days Represented","Confidence Rating", "Most recent kill/loss"]
        rtable=""
        rows=[]
        for i in mails:
            rows.append((i[4],i[1],i[3],i[5],i[2]))
        
            

        #response = "\r\n\r\n" + tabulate(rows, headers = rhead)

        self.sql.insertCachedReport(self.getSolReportType(), sol, str(rows))
        
        return rows

    def processSolReportKills(self, kills):
        #corp/AllianceID, kills+losses, last kill/loss, days represented(bugged by up to 2x off), name
        #confidence = 2**(daycount/2) *killcount * max( -.1 * (avgdelta*10 -24)**2 +5, 1)
        l=[]
        for i in kills:
            killCount=i[1]
            lastKill=i[2]
            daysRep=i[3]


            #print(lastKill)
            #lastKill=date(lastKill)
            lastKill= datetime.datetime.strptime(lastKill.replace("-","").replace(" ","").replace(":",""),'%Y%m%d%H%M%S')
            lastKill=lastKill.date()
            now =datetime.datetime.now().date()
            #print(now)
            #now=date()
            #print(type((now-lastKill).days))
            #print(type(killCount))
            #print(type(daysRep))

            #print(2**(daysRep/2.0))
            confidence= 2**(daysRep/2) * killCount * 1/max(1, 2**(((now-lastKill).days)/7) )
            confidence=int(confidence)
            #confidence=int(confidence*1000)
            #confidence=confidence/1000.0
            #print(confidence)

            
            l.append(list(i))
            #print(l[-1])
            l[-1].append(confidence)
            l[-1][3] = l[-1][3]/1 #divide days
            l[-1][2] = l[-1][2][0:10] #remove time from datetime 
            #i.append(confidence)
        
        l.sort(key = lambda x:x[-1], reverse = True)

        for i in range(len(l)):
            if(l[i][5]>=1000000):
                l[i][5]="Inf"
            if(False and len(l[i][4])<27):
                l[i][4] = l[i][4] +"_"*(27- len(l[i][4])) #pad with underscores 
        
        l = l[0:min(len(kills),10)] #take top 10 systems
        return l

    def findCharHome(self, eID, key, kills, losses):
        return self.findEntityHome(eID, key, kills+losses)

    def findCharHomeRaw(self, eID, key, kills, losses):
        return self.findEntityHomeRaw(eID, key, kills+losses)

    def findCharPeakTime(self, eID, key, kills, losses):
        return self.findEntityPeakTime(eID, key, kills, losses)

    def findCharDoctrines(self, eID, key, kills, losses):
        return self.findEntityDoctrines(eID, key, kills, losses)
            
    def findCorpHome(self, eID, key, kills, losses):
        return self.findEntityHome(eID, key, kills+losses)

    def findCorpPeakTime(self, eID, key, kills, losses):
        return self.findEntityPeakTime(eID, key, kills, losses)

    def findCorpDoctrines(self, eID, key, kills, losses):
        return self.findEntityDoctrines(eID, key, kills, losses)

    def findAllianceHome(self, eID, key, kills, losses):
        return self.findEntityHome(eID, key, kills+losses)

    def findAlliancePeakTime(self, eID, key, kills, losses):
        return self.findEntityPeakTime(eID, key, kills, losses)

    def findAllianceDoctrines(self, eID, key, kills, losses):
        return self.findEntityDoctrines(eID, key, kills, losses)
            
    def findEntityHome(self, eID, key, kills):
        #joint = kills+losses
        response =""
        #killHead = ["System", "NumKills+Losses", "DaysRepresented", "Avg Kill Delta(days)", "Confidence Rating", "Most recent kill/loss"]
        killHead = ["System", "NumKills+Losses", "DaysRepresented", "Class", "Confidence Rating", "Most recent kill/loss"]

        stats = self.findEntityHomeRaw(eID, key, kills)

        response = tabulate(stats, headers = killHead) 
        
        return response

    def findEntityHomeRaw(self, eID, key, kills):
        #joint = kills+losses
        r=self.sql.getCachedReport(self.getHomeReportType(), eID)
        if(len(r)>0):
            print("using cache")
            return literal_eval(r[0][0])
        response =""

        killTable = ""
        #killHead = ["System", "NumKills+Losses", "DaysRepresented", "Avg Kill Delta(days)", "Confidence Rating", "Most recent kill/loss"]
        killHead = ["System", "NumKills+Losses", "DaysRepresented", "Class", "Confidence Rating", "Most recent kill/loss"]
        killT = []
        
        zkill = 0
        system =1
        time =2
        
        systems ={}
        for i in kills:
            if(i[system] in systems):
                #print(str(i[system])+" "+str(systems[i[system]]))
                #wtf = 
                systems[i[system]].append(i)
            else:
                #print("adding "+ str(i[system]) +" "+str(i))
                systems[i[system]] = [i]
        
        stats =[]
        #print(systems.keys())
        for i in systems.keys():
            #for j in systems[i]:
            stats.append(self.processSystem(systems[i]))
        
        
        stats.sort(key = lambda x:x[4], reverse = True) #sort by confidence rating

        stats = stats[0:min(len(stats),15)] #take top 15 systems

        response = stats
        
        self.sql.insertCachedReport(self.getHomeReportType(), eID, str(response))

        return response

    
    def processSystem(self, system):
        
        #print(system)
##        if(len(system)>1):
##            print(system)
##            exit
        sysID = system[0][1]
        name = self.sql.getSolarNameBySolarID(sysID)[0][0]
        killcount = len(system)
        days={}
        daycount = 0

        dates = []
        unix = datetime.datetime(1970,1,1)
        
        for i in system:
            day =i[2]
            dates.append(datetime.datetime.strptime(day.replace("-","").replace(" ","").replace(":",""),'%Y%m%d%H%M%S'))
            day =i[2].split(" ")[0]
            if(day in days):
                days[day] = days[day] +1
            else:
                days[day]=1

        daycount = len(days)
        #day=[]
        dates.sort(reverse = True)
        delta = 0

        secondsInHr = 60*60
        secondsInDay = 60*60*24
        avgdelta = 0
        if(len(dates)>2):
            for i in range(1, len(dates)):
                #delta = delta +(i-unix).total_seconds()/(secondsInDay)
                delta = delta + (dates[i-1]-dates[i]).total_seconds()/(secondsInDay)
            avgdelta = (delta +0.0)/len(dates)
        if(len(dates)==2):
            avgdelta = (dates[0]-dates[1]).total_seconds()/2/(secondsInDay)

        avgdelta = float(int((avgdelta*1000))%1000)/1000


        lastKill = str(dates[0].year)+"-"+str(dates[0].month)+"-"+str(dates[0].day)
        now = datetime.datetime.now().date()
        confidence = 2**(daycount/2) *killcount *  1/max(1, 2**(((now-dates[0].date()).days)/7) )
        #max( -.1 * (avgdelta*10 -24)**2 +5, 1) *
        
        sysType = self.getSysClassByID(sysID)
        return (name, killcount, daycount, sysType, confidence, lastKill)

    def getSysClassByID(self, sysID):
        
        #thera =31000005 
        #c1 <=31000354
        #c2 <=31000879
        #c3 <=31001374
        #c4 <=31001879

        #c5-6 indexes buggy as fuck
        
        #c5 <=31002366 and <=31002504 -C6
        #c6 31002366 to 31002470 (inclusive)
        #shattered >=31002505
        if(sysID < 31000005):
            return "K space"
        if(sysID==31000005):
            return "Thera"
        if(sysID<=31000354):
            return "C1"
        if(sysID <=31000879):
            return "C2"
        if(sysID <=31001374):
            return "C3"
        if(sysID <= 31001879):
            return "C4"
        if((sysID >= 31002366 and sysID <=31002470) or (sysID ==31002487 or sysID ==31002489 or sysID ==31002492)):
            return "C6 (buggy)"
        if(sysID <=31002366 or sysID <=31002504):
            return "C5 (buggy)"
        return "Shattered"

        
    def findEntityPeakTime(self, eID, key, kills, losses):
        return "Peak Time not implemented"

    def findEntityDoctrines(self, eID, key, kills, losses):
        return "Doctrines not implemented"




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


    def getHomeReportType(self):
        return 1
    def getSolReportType(self):
        return 2
    def getLeadershipReportType(self):
        return 3
    def getHrsReportType(self):
        return 4
    def getSiegeReportType(self):
        return 5
    def isDBlocked(self):
        
        lastTOD = self.sql.sqlCommand("select max(timeofdeath) from kills")
        if(lastTOD is None or len(lastTOD)<=0):
            raise DBLockedException()
        lastTOD = self.sql.sqlCommand("select max(kill) from attackers")
        if(lastTOD is None or len(lastTOD)<=0):
            raise DBLockedException()

    def entityNotFound(self, entity):
        lastTOD = self.sql.sqlCommand("select max(timeofdeath) from kills")
        if(lastTOD is None or len(lastTOD)<=0):
            raise DBLockedException()
        raise EntityNotFoundException(entity, lastTOD[0][0])

    def getFunctionName(self):
        return str(inspect.currentframe().f_back.f_code.co_name)
    def invalidInputMsg(self, i, reportName):
        return "Input: "+str(i)+" invalid for report: "+str(reportName)+"\nBe sure you are requesting a report with arguments that make sense in the context of the report.\nRequesting a list of FCs makes sense for a corp, but not a character"

if(False):
    d = dataProcessingInterface()

    r =d.genReport("Marclass")
    print(r)

    r= d.genReport("Pos Party")
    print(r)

    r= d.genReport("Low-Class")
    print(r)

    r= d.genReport("lazerhawks")
    print(r)

    r= d.genReport("adfadfadfadfadsfadfasdfasdfasdf")
    print(r)
