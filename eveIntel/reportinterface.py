from eveIntel.dataprocessinginterface import dataProcessingInterface
from eveIntel.Exceptions import *



class reportInterface():
    def __init__(self):
        self.data = dataProcessingInterface()


    ##def getHomeRaw(entityName):
    ##    return data.genReport(entityName)

    def getHome(self, entityName):
        return self.reportOrErr(self.data.genReport, entityName)
    
    def getHomeReportRaw(self, entityName):
        return self.data.genReportRaw(entityName)
    
    def getSolReport(self, solName):
        return self.reportOrErr(self.data.genReport, solName)

    def getSolReportRaw(self, solName):
        return self.data.genReportRaw(solName)
    
    def getLeadershipReport(self, entityName):
        return self.reportOrErr(self.data.genLeadershipReport, entityName)
    
    def getLeadershipReportRaw(self, entityName):
        return self.data.genLeadershipReport(entityName)

    def getSiegeReport(self ):
        return self.data.genSiegeReport()

    def getSiegeReportRaw(self ):
        return self.data.genSiegeReport()
    
    def getHrsReport(self, entityName):
        return self.reportOrErr(self.data.genHrsReport, entityName)
    
    def getHrsReportRaw(self, entityName):
        return self.data.genHrsReport(entityName)
    
    def setDBConnection(self, connection):
        self.data.setDBConnection(connection)

    def reportOrErr(self, report, arg):
        try:
            return report(arg)
        except (EntityNotFoundException, DBLockedException) as e:
            return str(e)

        
    def toJson(data, headers):
        return ""

