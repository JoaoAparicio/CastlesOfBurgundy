import random

class EstateTile:
    def __init__(self,type=None,die=None):
        self.type = type
        self.die = die
        self.neighbor = []
        self.placement = None

class Estate:
    def __init__(self):
        self.e = initializeEstate()

    def findAvailableDie(self,n): ## returns list of EstateTiles with a given die number
        avai = []
        for estatetile in self.e:
            for neighbor in estatetile.neighbor:
                if neighbor.type == None and neighbor.die == n:
                    avai.append(neighbor)
        return avai

    def findAvailableType(self,type): ## returns list of EstateTiles with a given die number
        avai = []
        for i in self.e:
            for j in i.neighbor:
                if j.die2 == None and j.type == type:
                    avai.append(j)
        return avai

    def findAvailableTypeDie(self,type,n): ## returns list of EstateTiles with a given die number
        avai = []
        for i in self.e:
            for j in i.neighbor:
                if j.die2 == None and j.die == n and j.type == type:
                    avai.append(j)
        return avai

class PlayerBoard:
    def __init__(self):
        self.estate = Estate()
        self.storage = [None,None,None]
        self.goodsstorage = [[],[],[]]
        self.silverlingstorage = 0
        self.soldgoods = []

def initializeEstate():
    e = [0]
    for i in range(0,37):
        e.append(EstateTile())
    e[1].type = 'Green'
    e[1].die = 6
    e[1].neighbor = [e[2],e[5],e[6]]
    e[2].type = 'Dark Green'
    e[2].die = 5
    e[2].neighbor = [e[1],e[3],e[6],e[7]]
    e[3].type = 'Dark Green'
    e[3].die = 4
    e[3].neighbor = [e[2],e[3],e[7],e[8]]
    e[4].neighbor = [e[3],e[8],e[9]]
    e[5].type = 'Green'
    e[5].die = 2
    e[5].neighbor = [e[1],e[6],e[10],e[11]]
    e[6].type = 'Green'
    e[6].die = 1
    e[6].neighbor = [e[1],e[2],e[5],e[7],e[11],e[12]]
    e[7].type = 'Dark Green'
    e[7].die = 6
    e[7].neighbor = [e[2],e[3],e[6],e[8],e[12],e[13]]
    e[8].type = 'Yellow'
    e[8].die = 5
    e[8].neighbor = [e[3],e[4],e[7],e[9],e[13],e[14]]
    e[9].type = 'Beige'
    e[9].die = 4
    e[9].neighbor = [e[4],e[8],e[14],e[15]]
    e[10].type = 'Green'
    e[10].die = 5
    e[10].neighbor = [e[5],e[11],e[16],e[17]]
    e[11].type = 'Green'
    e[11].die = 4
    e[11].neighbor = [e[5],e[6],e[10],e[12],e[17],e[18]]
    e[12].type = 'Beige'
    e[12].die = 3
    e[12].neighbor = [e[6],e[7],e[11],e[13],e[18],e[19]]
    e[13].type = 'Yellow'
    e[13].die = 1
    e[13].neighbor = [e[7],e[8],e[12],e[14],e[19],e[20]]
    e[14].type = 'Beige'
    e[14].die = 2
    e[14].neighbor = [e[8],e[9],e[13],e[15],e[20],e[21]]
    e[15].type = 'Beige'
    e[15].die = 3
    e[15].neighbor = [e[9],e[14],e[21],e[22]]
    e[16].type = 'Blue'
    e[16].die = 6
    e[16].neighbor = [e[10],e[16],e[23]]
    e[17].type = 'Blue'
    e[17].die = 1
    e[17].neighbor = [e[10],e[11],e[16],e[18],e[23],e[24]]
    e[18].type = 'Blue'
    e[18].die = 2
    e[18].neighbor = [e[11],e[12],e[17],e[19],e[24],e[25]]
    e[19].type = 'Dark Green'
    e[19].die = 6
    e[19].neighbor = [e[12],e[13],e[18],e[20],e[25],e[26]]
    e[20].type = 'Blue'
    e[20].die = 5
    e[20].neighbor = [e[13],e[14],e[19],e[21],e[26],e[27]]
    e[21].type = 'Blue'
    e[21].die = 4
    e[21].neighbor = [e[14],e[15],e[20],e[22],e[27],e[28]]
    e[22].type = 'Blue'
    e[22].die = 1
    e[22].neighbor = [e[15],e[21],e[28]]
    e[23].type = 'Beige'
    e[23].die = 2
    e[23].neighbor = [e[16],e[17],e[24],e[29]]
    e[24].type = 'Beige'
    e[24].die = 5
    e[24].neighbor = [e[17],e[18],e[23],e[25],e[29],e[30]]
    e[25].type = 'Grey'
    e[25].die = 4
    e[25].neighbor = [e[18],e[19],e[24],e[26],e[30],e[31]]
    e[26].type = 'Beige'
    e[26].die = 3
    e[26].neighbor = [e[19],e[20],e[25],e[27],e[31],e[32]]
    e[27].type = 'Beige'
    e[27].die = 1
    e[27].neighbor = [e[20],e[21],e[26],e[28],e[32],e[33]]
    e[28].type = 'Green'
    e[28].die = 2
    e[28].neighbor = [e[21],e[22],e[27],e[33]]
    e[29].type = 'Beige'
    e[29].die = 6
    e[29].neighbor = [e[23],e[24],e[30],e[34]]
    e[30].type = 'Grey'
    e[30].die = 1
    e[30].neighbor = [e[24],e[25],e[29],e[31],e[34],e[35]]
    e[31].type = 'Yellow'
    e[31].die = 2
    e[31].neighbor = [e[25],e[26],e[30],e[32],e[35],e[36]]
    e[32].type = 'Grey'
    e[32].die = 5
    e[32].neighbor = [e[26],e[27],e[31],e[33],e[36],e[37]]
    e[33].type = 'Grey'
    e[33].die = 6
    e[33].neighbor = [e[27],e[28],e[32],e[37]]
    e[34].type = 'Grey'
    e[34].die = 3
    e[34].neighbor = [e[29],e[30],e[35]]
    e[35].type = 'Yellow'
    e[35].die = 4
    e[35].neighbor = [e[30],e[31],e[34],e[36]]
    e[36].type = 'Yellow'
    e[36].die = 1
    e[36].neighbor = [e[31],e[32],e[35],e[37]]
    e[37].type = 'Beige'
    e[37].die = 3
    e[37].neighbor = [e[32],e[33],e[36]]
    e.pop(0)
    return e

e = Estate()
print e.findAvailableDie(4)


