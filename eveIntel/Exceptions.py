


class FatalException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    




class GenericException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
class EntityNotFoundException(Exception):
    def __init__(self, entity, tod):
        self.entity = entity
        self.tod = tod
    def __str__(self):
        return "Entity: \""+ str(self.entity) +"\" has no kill/death history in w space as of "+str(self.tod)+"\nIf you believe this is in error verify that you are searching by the in game name exactly as it appears including trailing '.'"
    
class DBLockedException(Exception):
    def __init__(self):
        self=self
    def __str__(self):
        return repr("The DB appears to be locked. The previous day's kills are likely being processed, please wait a few minutes and try again.")
