#because changing the SDEConnector myself probably isnt the best option
#if I want to open source this thing later

from EveCommon.SDEConnector import SDEConnector




class sdeInterface():
    database_url = "D:\Eve Static DB\ESB.sqlite"
    sde = SDEConnector(db_name=database_url)
    

    def getSolarIDBySolarName(self, name):
            query = "select SOLARSYSTEMID from mapSolarSystems where SOLARSYSTEMNAME= ?"
            #name = [name]
            #name = "\'"+name+"\'"
            result = self.sde.execute_raw(query, [name]).fetchall()
            
            if(len(result)==0):
                    return None
            return result[0][0]


    def getSolarNameBySolarID(self, solarID):
            query = "select SolarSystemName from mapSolarSystems where SolarSystemID = ?"
            
            result = self.sde.execute_raw(query, (str(solarID),)).fetchall()
             
    
            if(len(result)==0):
                    return None
            return result[0][0]


    

