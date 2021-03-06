from eveIntel.zkillinterface import zKillInterface
from eveIntel.sqlinterface import sqlConnection
from eveIntel.evelinkinterface import evelinkinterface
from eveIntel.sdeinterface import sdeInterface

import time
from ast import literal_eval

evelink = evelinkinterface()
sql = sqlConnection()
sql.connect()
zkill = zKillInterface()
sde = sdeInterface()


def getAllianceList():
    return evelink.getAllianceList()


def populateAlliancesAndCorps():
    alliances = getAllianceList()
    a = alliances[0]
    for i in a.keys():
        
        sql.insertAlliance(a[i]["id"], a[i]["name"])
        for corp in a[i]["member_corps"].keys():
            sql.insertCorp(corp, "", a[i]["id"])
            


def pullWHKills():
    import datetime
    
    whstart = 31000007
    whend = 31002605

    
    startID = 31000005
    endID = 31002605
    thera = 31000005

    killNum = 0
    delta = 0
    print("Beginning WH km pull starting ID = "+ str(startID) +" end ID = "+str(endID))
    for i in range(startID, endID):
        if(i==31000006):
            continue
        kills=[]
        try:
            lastPulled = s("select max(timeofdeath) from kills where system = "+str(i))
            if(type(lastPulled)==list and len(lastPulled)>0):
                lastPulled = str(lastPulled[0][0])
            else:
                lastPulled = None

            if(lastPulled is not None):
                lastDate = datetime.datetime.strptime(lastPulled.replace("-","").replace(" ","").replace(":",""),'%Y%m%d%H%M%S')
                kills = zkill.getKillsInSystemBySystemID(i, start = lastDate)
            else:
                kills = zkill.getKillsInSystemBySystemID(i)
            killNum = killNum +len(kills)
            delta = len(kills)
            for kill in kills:
                sql.insertRawKM(kill.killID, str(kill.__dict__))
        except Exception as err:
            print("Error pulling kills for ID "+str(i))
            print("system name: "+ sde.getSolarNameBySolarID(str(i)))
            print("Err: "+ str(err))
            print("")
        
        print(str(killNum)+" kills processed")
        print(str(delta) +" kils for this wh")
        print("At ID "+str(i))
        print("system name: "+ sde.getSolarNameBySolarID(str(i))+"\n")
        time.sleep(2)



def populateNonKills():
    
    populateAlliancesAndCorps()
    #populateCorps()
    populateChars()


    sql.close()

def s(command):
    return sql.sqlCommand(command)


def processPulledKills():
    count  = sql.sqlCommand("select count(1) from killsraw where processed = 'False' and skipped = 'False'")[0][0]
    command = "select id, zkillid, killmail from killsraw where processed ='False' and skipped = 'False' Limit 50000;" #arg order doesnt get preserved in returned rows for some reason
    command = "select id, zkillid, killmail from killsraw where processed ='False' and skipped = 'False';" #arg order doesnt get preserved in returned rows for some reason
    rows = sql.sqlCommand(command)
    processedRows = 0
    skipped =0
    print("Beginning KM processing, count = "+str(count))

    for r in rows:
        success = processRawKill(r)
        if(success):
            sql.setRawKillProcessed(r[0])
            processedRows = processedRows +1
        else:
            sql.setRawKillSkipped(r[0])
            skipped = skipped+1
        if((processedRows+skipped)%1000==0):
            print(str(processedRows)+" processed so far out of "+str(count))
            print(str(skipped)+" skipped so far out of "+str(count))

            
    while(False and len(rows)>0):
        row = rows.pop()
        success = processRawKill(row)
        if(success):
            sql.setRawKillProcessed(row[0])
            processedRows = processedRows +1
        else:
            sql.setRawKillSkipped(row[0])
            skipped = skipped+1
        if(len(rows)%1000 ==0):
            print("processed : "+str(processedRows)+" out of: "+ str(count)+" skipped : "+str(skipped) +" % done: " + str((processedRows+skipped+0.0) / count *100))
            #sql.commit()
        if(len(rows)==0):
            print("processed : "+str(processedRows)+" out of: "+ str(count)+" skipped : "+str(skipped) +" % done: " + str((processedRows+skipped+0.0) / count *100))
            sql.commit()
            rows = sql.sqlCommand(command)
    print("beginning commit")
    sql.commit()
    #sql.sqlCommand("update reportCache set valid='False'")
    sql.invalidateReportCache()
    print("done processing pulled kills count = " +str(processedRows))
    
def processRawKill(row):
    if(False ):#len(row)<=3):
        print("bad row: "+str(row))
        return False

    insertCharsOnly = False
    updateOnly =True
    
    ID = row[0]
    zkillid = row[1]
    killmail = literal_eval(row[2])
    if(len(killmail) <8):
        print(str(zkillid) +" was malformed, skipping")
        return False
    vic = killmail["victim"]
    #vic keys
    #[u'corporationID', u'factionID', u'damageTaken', u'characterName', u'factionName', u'allianceName', u'allianceID', u'shipTypeID', u'corporationName', u'characterID']

##    if(vic["characterName"] ==''):
##        print("structure death, skipping id: "+ str(ID))
##        return False
    
    date = killmail["killTime"]
    #print(ID)
    #print(zkillid)
    #print(str(killmail))
    attackers = killmail["attackers"]
    system = killmail["solarSystemID"]

##    for i in attackers:
##        if(i["characterName"]==''):
##            print("structure involved in kill, skipping id: "+str(ID))
##            return False

    
    insertCharIfNotExist(vic)

    if(not insertCharsOnly):
        if(vic["allianceName"]!=''):
            sql.insertKill(zkillid, vic["characterID"], date, system, vic["corporationID"],  vic["shipTypeID"], alliance=vic["allianceID"])
            
        else:
            sql.insertKill(zkillid, vic["characterID"], date, system, vic["corporationID"],  vic["shipTypeID"])

    for i in attackers:
        insertCharIfNotExist(i)
        if(not insertCharsOnly ):
            insertAttacker(i, zkillid)


    
    #finish this shit

    return True


def insertCharIfNotExist(char):
    #
##    print("char: " +str(char["characterName"]) +"\n"+
##          "charID: "+ str(char["characterID"])+"\n"+
##          "corp: "+ str(char["corporationID"]) +"\n")
    
    if(char["characterName"]==''):
        return False #not processing modules yet
    if(char["characterID"]<31009000): #some killmails are bugged and list the system as a victim or attacker
        return False
    
    if(char["allianceName"] !=''):
        

         sql.insertAlliance(char["allianceID"],char["allianceName"])
        
    if(char["corporationID"] !=''):
        if(char["allianceName"]==''):


            sql.insertCorp(char["corporationID"], char["corporationName"])
        else:


            sql.insertCorp(char["corporationID"], char["corporationName"], alliance=char["allianceID"])


    sql.insertPlayer(char["characterID"],char["characterName"],char["corporationID"])


    return True


def insertAttacker(char, zkillID):
    #
    if(char["characterName"]!=''):
        if(char["allianceName"] ==''):
            sql.insertAttacker( char["characterID"], zkillID, char["damageDone"], char["corporationID"],char["shipTypeID"])
        else:
            sql.insertAttacker(char["characterID"], zkillID, char["damageDone"], char["corporationID"], char["shipTypeID"], allianceID=char["allianceID"])
    else:
        #npc
        if(char["allianceName"] ==''):
            sql.insertAttacker( 1, zkillID, char["damageDone"], char["corporationID"],char["shipTypeID"])
            
        else:
            sql.insertAttacker(1, zkillID, char["damageDone"], char["corporationID"], char["shipTypeID"], allianceID=char["allianceID"])


        
def populateSystems():
    start = 30000000
    end = 30006000
    count =0
    for i in range(start, end):
        name = sde.getSolarNameBySolarID(i)
        if(name is not None):
            #sql.sqlCommandParameterizedWithoutCommit("insert or ignore into systems (ccpID, name, lastPulled) values(?, ?, date('2015-03-18'));", (str(i), name))
            sql.insertSystem(i, name)
            count = count+1
    print(str(count)+" k space systems added")

    sql.commit()
    thera = 31000005
    whstart = 31000007
    whend = 31002605
    wcount = 0
    for i in range(thera, whend):
        name = sde.getSolarNameBySolarID(i)
        if(name is not None):
            #sql.sqlCommandParameterizedWithoutCommit("insert or ignore into systems (ccpID, name, lastPulled) values(?, ?, date('2015-03-18'));", (str(i), name))
            sql.insertSystem(i, name)
            wcount = wcount+1
    sql.commit()
    print(str(wcount)+" w space systems added")

    print(str(count + wcount) +" total systems added")
            

    
#x = sql.sqlCommand("select * from alliances where rowid <=5")
#print(sql.sqlCommand("select * from alliances where rowid <=5"))



#sql.close()
#print(sql.sqlCommand(""))
pullWHKills()
#populateSystems()
processPulledKills()
