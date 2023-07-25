#Class to hold information regarding a specific peak
#################################################################
class Sample:
    def __init__(self, _pc, _sn, _rt):
        self.pc = _pc
        self.sn = _sn
        self.rt = float(_rt)

    def getPC(self):
        return self.pc

    def getSN(self):
        return self.sn
    
    def getRT(self):
        return self.rt
#################################################################
