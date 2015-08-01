from eveIntel.evelinkinterface import evelinkinterface
from eveIntel.sqlinterface import sqlConnection
from tabulate import tabulate
from eveIntel.sdeinterface import sdeInterface

import time
from datetime import date
import datetime

#Characters: ]90000000, 98000000[ ## only applies to stuff made after 64 bit
#Corporations: ]98000000, 99000000[ ## move, older shit will not fall in
#Alliances: ]99000000, 100000000[## these ranges :(
class dataProcessingInterface():
    eve  = evelinkinterface()
    sql = sqlConnection()
    sql.connect()
    sde = sdeInterface()

    homeHeader=["System", "#Kills", "#Losses", "Kill dt avg",
                "Loss dt avg", "Kill dt variance", "Loss dt variance",
                "First Kill/Loss", "Last Kill/Loss", "Certainty"]
    def genReport(self, entity):
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
            return self.genCharReport(entityID)
        elif(self.isCorp(entityID)):
            end  = int(time.time())
            print("isX took: "+str(end-start)+"")
            return self.genCorpReport(entityID)
        elif(self.isAlliance(entityID)):
            end  = int(time.time())
            print("isX took: "+str(end-start)+"")
            return self.genAllianceReport(entityID)
        elif(self.isSystem(entityID)):
            end  = int(time.time())
            print("isX took: "+str(end-start)+"")
            return self.genSolReport(entityID)
        else:
            lastTOD = self.sql.sqlCommand("select max(timeofdeath) from kills")

            if(len(lastTOD)>0):
                lastTOD=lastTOD[0][0]
            else:
                return "The DB appears to be locked. The previous day's kills are likely being processed, please wait a few minutes and try again."
            
            return "Entity: \""+ str(entity) +"\" has no kill/death history in w space as of "+str(lastTOD)
        return report


    def isChar(self, entityID):
        if(int(entityID)>=90000000 and int(entityID <98000000)):
            return True
        return len(self.sql.getCharacterByCCPID(entityID)) >0
        #return False

    def isCorp(self, entityID):
        if(int(entityID)>=98000000 and int(entityID <99000000)):
            return True
        return len(self.sql.getCorpByCCPID(entityID)) >0
        
        #return False
        
    def isAlliance(self, entityID):
        if(int(entityID)>=99000000 and int(entityID <100000000)):
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

        report =""
        
        kills = self.sql.getKillsAndLossesByCharacter(char)
        #print(type(kills))
        #print(kills)
        if(type(kills) == str):
            return kills
        home = self.findCharHome(char, key, kills, [])
        report = home+"\r\n"
        return report

    def genCorpReport(self, corp):
        key = "corporationID"
        report =""
        start = int(time.time())
        
        kills = self.sql.getKillsAndLossesByCorp(corp)

        end = int(time.time())

        print("elapsed time was "+str(end-start) +" seconds to pull kills for corp: "+str(corp))
        if(type(kills) == str):
            return kills

        start = int(time.time())
        
        home = self.findCharHome(corp, key, kills, [])
        end = int(time.time())

        print("elapsed time was "+str(end-start) +" seconds to process kills for corp: "+str(corp))
        
        report = home+"\r\n"
        return report

    def genAllianceReport(self, alliance):
        key = "allianceID"
        report =""

        start = int(time.time())
        
        kills = self.sql.getKillsAndLossesByAlliance(alliance)

        end = int(time.time())

        print("elapsed time was "+str(end-start) +" seconds to pull kills for corp: "+str(alliance))
        
        if(type(kills) == str):
            return kills
        
        home = self.findCharHome(alliance, key, kills, [])
        report = home+"\r\n"
        return report

    def genLeadershipReport(self, entity):
        print("Leadership Report for: "+ entity)
        entityID = self.sql.getEntityID(entity)
        
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
            return "You have given a character. Leadership reports are allowed for corporations or alliances only"
        elif(self.isCorp(entityID)):
            end  = int(time.time())
            print("isX took: "+str(end-start)+"")
            return self.genCorpLeadershipReport(entityID)
        elif(self.isAlliance(entityID)):
            end  = int(time.time())
            print("isX took: "+str(end-start)+"")
            return self.genAllianceLeadershipReport(entityID)
        
        else:
            lastTOD = self.sql.sqlCommand("select max(timeofdeath) from kills")

            if(len(lastTOD)>0):
                lastTOD=lastTOD[0][0]
            else:
                return "The DB appears to be locked. The previous day's kills are likely being processed, please wait a few minutes and try again."
            
            return "Entity: \""+ str(entity) +"\" has no kill/death history in w space as of "+str(lastTOD)
        return "A failure state that should never have been reached was reached. Either your entity is not a corporation or alliance, or it has no killboard history in w space"
    
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
        rtable=""
        players = sqlCall(eID)

        sort = self.processLeadershipReport(players)
        rows=[]
        for i in sort:
            rows.append((i[1],i[2],i[3],i[4],i[5],i[6]))
        response = tabulate(rows, headers = rhead)

        return response

    def processLeadershipReport(self, rows):
        l=[]

        for i in rows:
            #calc confidence and append it to row then sort by confidence
            killCount = i[2]
            totalKills = i[3]
            fightPercent =i[3]
            fightNum = i[4]
            #print(i)
            
            confidence = fightPercent**2 * 2**(fightNum/4)

            l.append(list(i))
            
            l[-1].append(confidence)

        l.sort(key = lambda x:x[-1], reverse = True)

        return l[:15]
        
    def genSolReport(self, sol):
        key = "solarSystemID"

        kills = self.sql.getKillsAndLossesBySystem(sol)
        mails = self.processSolReportKills(kills)
        rhead =["corporation", "Kills+losses", "Days Represented","Confidence Rating", "Most recent kill/loss"]
        rtable=""
        rows=[]
        for i in mails:
            rows.append((i[4],i[1],i[3],i[5],i[2]))
        
            

        response = "\r\n\r\n" + tabulate(rows, headers = rhead)

        
        return response

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
            confidence= 2**(daysRep/2) * killCount * 1/max(1, 2**(((now-lastKill).days)/14) )
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
            if(len(l[i][4])<27):
                l[i][4] = l[i][4] +"_"*(27- len(l[i][4])) #pad with underscores 
        
        l = l[0:min(len(kills),10)] #take top 10 systems
        return l

    def findCharHome(self, eID, key, kills, losses):
        return self.findEntityHome(eID, key, kills+losses)

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

        killTable = ""
        killHead = ["System", "NumKills+Losses", "DaysRepresented", "Avg Kill Delta(days)", "Confidence Rating", "Most recent kill/loss"]
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

        response = response + "\r\n\r\n" + tabulate(stats, headers = killHead) 
        
        return response
    
    def processSystem(self, system):
        
        #print(system)
##        if(len(system)>1):
##            print(system)
##            exit
        name = system[0][1]
        name = self.sde.getSolarNameBySolarID(name)
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

        confidence = 2**(daycount/2) *killcount * max( -.1 * (avgdelta*10 -24)**2 +5, 1)
        lastKill = str(dates[0].year)+"-"+str(dates[0].month)+"-"+str(dates[0].day)
        return (name, killcount, daycount, avgdelta, confidence, lastKill)
        


        
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
