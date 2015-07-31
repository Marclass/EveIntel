from evelink import *
from evelink.corp import *
from evelink.api import *
from evelink.eve import *
import evelink


class evelinkinterface():
    eve =evelink.eve.EVE()
    api = evelink.api.API()
    corp = evelink.corp.Corp(api)
    def getCorpIDFromName(self, name):
        #
        
        charid = self.eve.character_id_from_name(name)
        return charid





    def getCharNameFromID(self, i):
        
        #
        return self.eve.character_name_from_id(i)






    def resolveNameFromID(self, i):
        result = self.getCharNameFromID(i)
        if(len(result)>0):
            return result[0]
        
        return None 


    def resolveIDFromName(self, name):
        #returns NONE for alliances
        result = self.getCorpIDFromName(name)
        if(len(result)>0):
            return result[0]
        return None


    def getEntityTypeFromID(self, entity):
        #t = self.eve.
        return ""


    def getAllianceList(self):
        return self.eve.alliances()

    def getCorpSheet(self, corpID):
        return self.corp.corporation_sheet(corp_id = corpID)

    def getCorpMemberList(self, corpID):
        return self.corp.members()

    
    test = False
    if(test):
        print(getCorpIDFromName("marclass"))
        print(resolveNameFromID(170700491))
        print(resolveIDFromName("Pos Party"))
        print(getCharNameFromID(170700491))
        x=getCorpIDFromName("Pos Party")
        print(len(x))
        #print(resolveIDFromName())
