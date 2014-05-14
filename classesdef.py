## VP aren't being taken into account properly.
## completely implemented sciences: 2,3 (but not activated)


import random, copy

logandexecute = False

# types: knowledge (yellow), ship (blue), animal (green), castle (dark green), mine (grey), building (beige)
# subtypes: non-existant for ships, castles and mines.
#           for animals, it's the type of animal and number: ['Cows', 3]
#           the knowledge it's just the number as specified by the manual (i.e. a number from 1 to 26)
#           for building it's one of the following: 'Warehouse', 'Carpenter's Workshop', 'Church', 'Market', 'Boarding House', 'Bank', 'City Hall', 'Watchtower' 
class SixSidedTile:
    def __init__(self,type,blackback,*subtype):
        self.type = type
        self.subtype = subtype
        self.blackback = blackback

    def __str__(self):
        return 'type='+self.type+' subtype='+str(self.subtype)+' blackback='+str(self.blackback)

# in the case of Goods Tiles, type is just a number 1-6
class GoodsTile:
    def __init__(self,type):
        self.type = type

def flatten(x):
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result


######## given a list, return randomly ordered version of that list #####
###### destroys the original
def scramblelist(x):
    temp = []
    for i in range(0,len(x)):
        r = random.randint(0,len(x)-1)
        temp.append(x[r])
        x.pop(r)
    return temp

def initializepiles(n):
    ''' Instanciate the correct number of each tile.'''
    blackback = []
    shipspile = []
    for i in range(0,20):
        shipspile.append(SixSidedTile('Blue',False))
    for i in range(0,6):
        blackback.append(SixSidedTile('Blue',True))

    minespile = []
    for i in range(0,10):
        minespile.append(SixSidedTile('Grey',False))
    for i in range(0,2):
        blackback.append(SixSidedTile('Grey',True))

    castlespile = []
    for i in range(0,16-n): ## subtract a number of castles equal to the n of players because
                          ## each player starts with 1 castle
        castlespile.append(SixSidedTile('Dark Green',False))
    for i in range(0,2):
        blackback.append(SixSidedTile('Dark Green',True))

    knowledgespile = []
    for i in range(1,7):
        knowledgespile.append(SixSidedTile('Yellow',False,i))
    blackback.append(SixSidedTile('Yellow',True,7))
    for i in range(8,12):
        knowledgespile.append(SixSidedTile('Yellow',False,i))
    blackback.append(SixSidedTile('Yellow',True,12))
    knowledgespile.append(SixSidedTile('Yellow',False,13))
    blackback.append(SixSidedTile('Yellow',True,14))
    blackback.append(SixSidedTile('Yellow',True,15))
    for i in range(16,24):
        knowledgespile.append(SixSidedTile('Yellow',False,i))
    blackback.append(SixSidedTile('Yellow',True,24))
    blackback.append(SixSidedTile('Yellow',True,25))
    knowledgespile.append(SixSidedTile('Yellow',False,26))

    ############## THE NUMBER OF ANIMALS IS WRONG ATM ##############
    animalspile = []
    animalspile.append(SixSidedTile('Green',False,'Cows',2))
    animalspile.append(SixSidedTile('Green',False,'Cows',3))
    animalspile.append(SixSidedTile('Green',False,'Cows',4))
    animalspile.append(SixSidedTile('Green',False,'Sheep',2))
    animalspile.append(SixSidedTile('Green',False,'Sheep',3))
    animalspile.append(SixSidedTile('Green',False,'Sheep',4))
    animalspile.append(SixSidedTile('Green',False,'Pigs',2))
    animalspile.append(SixSidedTile('Green',False,'Pigs',3))
    animalspile.append(SixSidedTile('Green',False,'Pigs',4))
    animalspile.append(SixSidedTile('Green',False,'Chicken',2))
    animalspile.append(SixSidedTile('Green',False,'Chicken',3))
    animalspile.append(SixSidedTile('Green',False,'Chicken',4))

    buildingspile = []
    buildingtypes = ['Warehouse', "Carpenter's Workshop", 'Church', 'Market', 'Boarding House', 'Bank', 'City Hall', 'Watchtower']
    for i in range(1,7):
        for type in buildingtypes:
            buildingspile.append(SixSidedTile('Beige',False,type))
    for i in range(7,9):
        for type in buildingtypes:
            blackback.append(SixSidedTile('Beige',True,type))

    animalspile = scramblelist(animalspile)
    knowledgespile = scramblelist(knowledgespile)
    buildingspile = scramblelist(buildingspile)
    blackback = scramblelist(blackback)

    goodstilespile = []
    for i in range(1,7):
        for j in range(1,8):
            goodstilespile.append(GoodsTile(i))
    goodstilespile = scramblelist(goodstilespile)

    pile = {'ships':shipspile, 'castles':castlespile, 'mines':minespile,'animals':animalspile,'knowledges':knowledgespile,'buildings':buildingspile,'blackback':blackback,'goodstiles':goodstilespile}

    return pile

class Gameboard:
    def __init__(self,n):
        self.nplayers = n
        self.turn = 0
        self.pile = initializepiles(self.nplayers)
        self.phasespaces = {'A':self.pile['goodstiles'][0:5],'B':self.pile['goodstiles'][5:10],'C':self.pile['goodstiles'][10:15],'D':self.pile['goodstiles'][15:20],'E':self.pile['goodstiles'][20:25]}
        self.roundspaces = []
        self.depots = {1:{'goods':[],1:None,2:None,3:None,4:None}, 2:{'goods':[],1:None,2:None,3:None,4:None}, 3:{'goods':[],1:None,2:None,3:None,4:None}, 4:{'goods':[],1:None,2:None,3:None,4:None}, 5:{'goods':[],1:None,2:None,3:None,4:None}, 6:{'goods':[],1:None,2:None,3:None,4:None}}
        self.blackdepot = {1:None,2:None,3:None,4:None,5:None,6:None,7:None,8:None}
         

class EstateTile:
    def __init__(self,type=None,die=None,pos=None):
        self.type = type
        self.die = die
        self.neighbor = []
        self.placement = None
        self.pos = None

class Estate:
    ''' Collection of properly initiallized EstateTiles and their respective zones.'''

    def __init__(self):
        self.e = initializeEstate()
        self.zones = initializeZones(self.e)

    def countMines(self):
        ''' Returns number of Mines in the Estate '''
        counter = 0
        for estatetile in self.e:
            if not estatetile.placement == None:
                if estatetile.placement.type == 'Grey':
                    counter += 1
        return counter

    def whichzone(self,n):
        ''' Given an EstateTile number n, returns the zone index the 
        EstateTile belongs to'''
        for nzone,zone in enumerate(self.zones):
            if self.e[n] in zone:
                return nzone

    def countAnimalsInAZone(self,animal,nzone):
        ''' Returns how many animals of a certain type are in
        a certain zone number n.'''
        counter = 0
        for estatetile in self.zones[nzone]:
            if not estatetile.placement == None:
                if estatetile.placement.subtype[0] == animal:
                    counter += estatetile.placement.subtype[1]
        return counter

    def zoneSubtypeAvailable(self,subtype,nzone):
        ''' Returns True if a certain zone number nzone is 
        available to place a certain subtype of type Beige, and
        False if it isn't.'''
        for estatetile in self.zones[nzone]:
            if not estatetile.placement == None:
                if estatetile.placement.subtype == subtype:
                    return False
        return True

    def ntiles(self):
        ''' Returns total number of EstateTiles placed.'''
        counter = 0
        for tile in self.e:
            if not tile.placement == None:
                counter += 1
        return counter

    def findAvailableDie(self,die):
        ''' Returns list of EstateTiles with a given die number.'''
        avai = []
        for estatetile in self.e:
            if not estatetile.placement == None:
                for neighbor in estatetile.neighbor:
                    if neighbor.placement == None and neighbor.die == die:
                        avai.append(neighbor)
        return avai

    def findAvailableType(self,type):
        ''' Returns list of EstateTiles with a given type.'''
        avai = []
        for estatetile in self.e:
            if not estatetile.placement == None:
                for neighbor in estatetile.neighbor:
                    if neighbor.placement == None and neighbor.type == type:
                        avai.append(neighbor)
        return avai

    def findAvailableTypeDie(self,type,die):
        ''' Returns list of EstateTiles with a given die number and type.'''
        avai = []
        for estatetile in self.e:
            if not estatetile.placement == None:
                for neighbor in estatetile.neighbor:
                    if neighbor.placement == None and neighbor.type == type and neighbor.die == die:
                        avai.append(neighbor)
        return avai

    def findAvailableTypeDieN(self,type,die):
        ''' Returns list of EstateTiles indexes with a given die number and type.'''
        avai = []
        for estatetile in self.e:
            if not estatetile.placement == None:
                for neighbor in estatetile.neighbor:
                    if neighbor.placement == None and neighbor.type == type and neighbor.die == die:
                        avai.append(neighbor.pos)
        return avai

    def findAvailableAll(self):
        ''' Returns list of all non-occupied EstateTiles.'''
        avai = []
        for estatetile in self.e:
            if not estatetile.placement == None:
                for neighbor in estatetile.neighbor:
                    if neighbor.placement == None:
                        avai.append(neighbor)
        return avai

    def checkTileSelfConsistency(self):
        for tile in self.e:
            for neighbor in tile.neighbor:
                if not tile in neighbor.neighbor:
                    print 'self consistency fail: Estatetile ',tile.type, tile.die,'has',neighbor.type, neighbor.die,' on its neighbor list, but not vice-versa'

    def checkZoneSelfConsistency(self):
        for zone in self.zones:
            for tile in zone:
                if not tile in self.e:
                    print 'self consistency fail: EstateTile ', tile.type,tile.die,'is in a zone but not in the estate list'
        for tile in self.e:
            found=False
            for zone in self.zones:
                if tile in zone:
                    found=True
            if found == False:
                 print 'self consistency fail: EsateTile',tile.type,tile.die,'is not in any zone'


class FuncObj(object):
        def __init__(self,name,args,kwargs):
                self.name = name;
                self.args = args;
                self.kwargs = kwargs;

        def __str__(self):
                return '{}{}'.format(self.name,self.args);

        def __repr__(self):
                return self.__str__();

        def call(self, parent=None):
                global logandexecute
                logandexecute = True
                if parent == None:
                    getattr(self.args[0], self.name)(*self.args[1:]);
                else:
                    getattr(parent, self.name)(*self.args[1:])

def log(func):
        def logger(*args, **kwargs):
                obj = args[0];
                funcObj = FuncObj(func.__name__, args, kwargs);
#                print(funcObj);
                if logandexecute == True:
                    obj.called.append(funcObj)
                    return func(*args, **kwargs)
                else:
                    obj.options.append(funcObj)
        return logger

class PlayerBoard:
    def __init__(self,n):
        self.n = n
        self.estate = Estate()
        castle = SixSidedTile('Dark Green',False)
        self.estate.e[18].placement = castle
        self.storage = []
        self.goodsstorage = [[],[],[]]
        self.silverlingstorage = 1
        self.soldstorage = []
        self.dice = []
        self.worker = n

class Game:
    ''' Game object, does everything a game master would do:
    increment turns, distribute tiles and silverlings, etc.'''

    def __init__(self,n):
        self.turn = 0
        self.phase = None
        self.nplayers = n
        self.gameboard = Gameboard(n)
        self.player = []
        for i in range(0,self.nplayers):
            self.player.append(Player(i+1,self.gameboard))
            for k in range(0,3):
                good = self.gameboard.pile['goodstiles'].pop(0)
                for stor in self.player[i].playerboard.goodsstorage:
                    if stor:
                       if stor[0].type == good.type:
                            stor.append(good)
                            break
                    else:
                        stor.append(good)
                        break
                
#        self.player1 = Player(1,self.gameboard)
#        self.player2 = Player(2,self.gameboard)
#        self.turnorder = [[self.player1,self.player2],[],[],[],[],[],[]]
        self.turnorder = [[self.player[0]],[],[],[],[],[],[]]

    def advance(self,player):
        ''' Advances a player in the turn order.'''
        for nturn,turn in enumerate(self.turnorder):
            if player in turn:
                turn.pop(turn.index(player))
                self.turnorder[nturn+1] = [player]+self.turnorder[nturn+1]
                break

    def incturn(self):
        ''' Increments turn.
        Distributes tiles, players roll dice, explores possible actions,
        executes an action according to player strategy.'''
        self.turnDistributeStuff()
        global logandexecute
        for i in self.turnorder:
            for player in i:
                player.sold = False
#                print player.playerboard.storage
                print player.playerboard.goodsstorage
                player.roll()
                logandexecute = False
                l = player.explore()
                player.strat(player,l)

    def distributesilverlings(self):
        ''' Distributes silverlings according to player's number of Mines.'''
        for np,p in enumerate(self.player):
            nmines = p.playerboard.estate.countMines()
            if p.science[2]:
                p.playerboard.silverlingstorage += nmines
                p.playerboard.worker += nmines
                print 'Player',np,'received',nmines,'silverlings and',nmines,'workers'
            else:
                p.playerboard.silverlingstorage += nmines
                print 'Player',np,'received',nmines,'silverlings'
        
    def turnDistributeStuff(self):
        gb = self.gameboard
        ### if new phase, distribute goods
        if self.turn == 0:
            self.phase = 'A'
        if self.turn == 5:
            self.distributesilverlings()
            self.phase = 'B'
        if self.turn == 10:
            self.distributesilverlings()
            self.phase = 'C'
        if self.turn == 15:
            self.distributesilverlings()
            self.phase = 'D'
        if self.turn == 20:
            self.distributesilverlings()
            self.phase = 'E'
        if self.turn == 0 or self.turn == 5 or self.turn == 10 or self.turn == 15 or self.turn == 20:
            for i in gb.phasespaces[self.phase]:
                gb.roundspaces.append(i)
            gb.phasespaces[self.phase] = []
            if self.nplayers >= 2:
                gb.depots[1][2] = gb.pile['buildings'].pop(0)
                gb.depots[1][3] = gb.pile['ships'].pop(0)
                gb.depots[2][1] = gb.pile['knowledges'].pop(0)
                gb.depots[2][3] = gb.pile['castles'].pop(0)
                gb.depots[3][1] = gb.pile['animals'].pop(0)
                gb.depots[3][3] = gb.pile['buildings'].pop(0)
                gb.depots[4][2] = gb.pile['ships'].pop(0)
                gb.depots[4][3] = gb.pile['buildings'].pop(0)
                gb.depots[5][2] = gb.pile['mines'].pop(0)
                gb.depots[5][4] = gb.pile['knowledges'].pop(0)
                gb.depots[6][2] = gb.pile['buildings'].pop(0)
                gb.depots[6][4] = gb.pile['animals'].pop(0)
                gb.blackdepot[2] = gb.pile['blackback'].pop(0)
                gb.blackdepot[4] = gb.pile['blackback'].pop(0)
                gb.blackdepot[5] = gb.pile['blackback'].pop(0)
                gb.blackdepot[7] = gb.pile['blackback'].pop(0)
            if self.nplayers >= 3:
                gb.depots[1][1] = gb.pile['knowledges'].pop(0)
                gb.depots[2][2] = gb.pile['buildings'].pop(0)
                gb.depots[3][2] = gb.pile['ships'].pop(0)
                gb.depots[4][4] = gb.pile['animals'].pop(0)
                gb.depots[5][1] = gb.pile['buildings'].pop(0)
                gb.blackdepot[1] = gb.pile['blackback'].pop(0)
                gb.blackdepot[8] = gb.pile['blackback'].pop(0)
#            if self.nplayers == 2 or self.nplayers == 4: # exception from the bottom of page 3
            if self.nplayers == 4: # exception from the bottom of page 3
                gb.depots[6][1] = gb.pile['castles'].pop(0)
            if self.nplayers == 3:
                if self.phase == 'A' or self.phase == 'C' or self.phase == 'E':
                    gb.depots[6][1] = gb.pile['castles'].pop(0)
                if self.phase == 'B' or self.phase == 'D':
                    gb.depots[6][1] = gb.pile['mines'].pop(0)
            if self.nplayers >= 4:
                gb.depots[1][4] = gb.pile['animals'].pop(0)
                gb.depots[2][4] = gb.pile['buildings'].pop(0)
                gb.depots[3][4] = gb.pile['knowledges'].pop(0)
                gb.depots[4][1] = gb.pile['mines'].pop(0)
                gb.depots[5][3] = gb.pile['buildings'].pop(0)
                gb.depots[6][3] = gb.pile['ships'].pop(0)
                gb.blackdepot[3] = gb.pile['blackback'].pop(0)
                gb.blackdepot[6] = gb.pile['blackback'].pop(0)

        self.turn += 1

        ### roll white die and place goods in depots
        gb.whitedie = random.randint(1,6)
        x = gb.roundspaces.pop(len(gb.roundspaces)-1)
        gb.depots[gb.whitedie]['goods'].append(x)
        self.printturn()

    def printturn(self):
        print '************* turn',self.turn,'phase',self.phase,'*************'



class Player:
    def __init__(self,n,gameboard):
        self.playernumber = n
        self.playerboard = PlayerBoard(n)
        self.gameboard = gameboard
        self.vp = 0 # victory points
        self.options = []
        self.decisions = []
        self.called = []
        self.funcobj = None
        self.verbose = False
        self.strat = None     ## strategy to use. this has to be assigned once, from the outside.
        self.effect = None    ## last effect
        self.sold = False     ## False if you've sold before this turn, and True if you haven't
        self.science = [0,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]

    def explore(self):
        ''' Returns list of all final states that can be obtained from 
        self by playing given dice.'''
#        print self.effect
        global logandexecute
        forks = []
        results = []
        logandexecute = False
        self.findOptions()
#        if self.options:
#            print self.options
        for i in self.options:
            forks.append(copy.deepcopy(self))
        for ni,i in enumerate(forks):
            logandexecute = True
            i.options[ni].call()
            logandexecute = False
            results.append(i.explore())
        if not self.options:
            return [ self ]
        else:
            return flatten(results)

    def roll(self):
        ''' Roll dice.'''
        self.playerboard.dice = [random.randint(1,6),random.randint(1,6)]
        print 'Player',self.playernumber,'rolled',self.playerboard.dice

    @log
    def effectAdd4Workers(self):
        self.playerboard.worker += 4

    @log
    def actionTakeWorkerTiles(self,ndie):
        ''' Exchanges n-th die for a worker.'''
        if self.verbose:
            print 'Exchanging die',self.playerboard.dice[ndie],'by 2 workers'
        self.playerboard.dice.pop(ndie)
        self.playerboard.worker += 2
        if self.science[13]:
            if self.verbose:
                print '... and one silverling (science 13)'
            self.playerboard.silverlingsstorage += 1
        if self.science[14]:
            if self.verbose:
                print '... and two workers more (science 14)'
            self.playerboard.worker += 2

    @log
    def actionAddSixSidedTileToYourEstate(self, ndie,nstorage,nestatetile,usedie=True):
        sixsidedtile = self.playerboard.storage.pop(nstorage)
        self.playerboard.estate.e[nestatetile].placement = sixsidedtile
        if usedie:
            die = self.playerboard.dice.pop(ndie)
            if self.verbose:
                print 'Using die',die,', take from storage tile of type',sixsidedtile.type,sixsidedtile.subtype,'and place it on estate tile number',nestatetile
        else:
            self.effect = None
            if self.verbose:
                print 'Effect: take from storage tile of type',sixsidedtile.type,sixsidedtile.subtype,'and place it on estate tile number',nestatetile
        
        if sixsidedtile.type == 'Dark Green':
            self.effect = sixsidedtile
        if sixsidedtile.type == 'Green':
            animal = sixsidedtile.subtype[0]
            zone = self.playerboard.estate.whichzone(nestatetile)
##            if self.science[7]:
            self.vp += self.playerboard.estate.countAnimalsInAZone(animal,zone)
#            print 'VP increment!'
        if sixsidedtile.type == 'Beige':
            if sixsidedtile.subtype[0] == 'Boarding House':
                self.playerboard.worker += 4
                if self.verbose:
                    print 'Placed Boarding House, received 4 workers'
            if sixsidedtile.subtype[0] == 'Bank':
                self.playerboard.silverlingstorage += 2
                if self.verbose:
                    print 'Placed Bank, received 2 silverlings'
            if sixsidedtile.subtype[0] == 'Watchtower':
                self.vp += 4
#                print 'VP increment!'
                if self.verbose:
                    print 'Placed Watchtower, received 4 victory points'
            if sixsidedtile.subtype[0] in ["Carpenter's Workshop", 'Church', 'Market', 'City Hall']:
                self.effect = sixsidedtile


    @log
    def convertWorker(self,ndie,direction):
         ''' Spend 1 worker to add or subtract 1 from a die number.'''
         self.playerboard.worker -= 1
         if self.playerboard.dice[ndie] == 6 and direction == +1:
             self.playerboard.dice[ndie] = 1
             if self.verbose:
                 print 'Using worker to convert die: 6 -> 1'
             return None
         if self.playerboard.dice[ndie] == 1 and direction == -1:
             self.playerboard.dice[ndie] = 6
             if self.verbose:
                 print 'Using worker to convert die: 1 -> 6'
             return None
         if self.verbose:
             print 'Using worker to convert die:',self.playerboard.dice[ndie],'->',self.playerboard.dice[ndie]+direction
         self.playerboard.dice[ndie] += direction

    @log
    def actionTakeSixSidedTileFromTheGameboard(self,ndepot,nspace,usedie=True):
        sixsidedtile = self.gameboard.depots[ndepot][nspace]
        self.playerboard.storage.append(sixsidedtile)
#        if sixsidedtile == None:
#           print 'ADDED None TO THE STORAGE!'
        self.gameboard.depots[ndepot][nspace] = None
        if usedie == True:
            i = self.playerboard.dice.index(ndepot)
            die = self.playerboard.dice.pop(i)
            if self.verbose:
                print 'Using die',die,', take from depot',ndepot,'space',nspace,'a tile of type',sixsidedtile.type,sixsidedtile.subtype
        else:
            self.effect = None
            if self.verbose:
                print 'Effect: from depot',ndepot,', space',nspace,' take a tile of type',sixsidedtile,sixsidedtile.subtype

    @log
    def actionTakeFromBlackdepot(self,ndepot):
        ''' Take a tile from the blackdepot and place it in storage.'''
        sixsidedtile = self.gameboard.blackdepot[ndepot]
        self.gameboard.blackdepot[ndepot] = None
        self.playerboard.storage.append(sixsidedtile)
        self.playerboard.silverlingstorage -= 2
        if self.verbose:
            print 'Using sterlings take from blackdepot',ndepot,'a tile of type',sixsidedtile.type,sixsidedtile.subtype

    @log
    def effectDarkGreen(self,die):  ## as the effect of placing a dark green tile, you get a die
        if self.verbose:
            print 'Effect (Dark Green) adding extra die',die
        self.playerboard.dice.append(die)
        self.effect = None


    def findOptions(self): 
        ''' Find possible moves in a certain playerboard.'''
        self.options = []
        pb = self.playerboard

        if self.effect == None:
            ### STEAL FROM THE GAMEBOARD AND PLACE IN STORAGE
            if len(pb.storage) < 3:
                for die in pb.dice:
                    for i in range(1,5):
                        if not self.gameboard.depots[die][i] == None:
                            self.actionTakeSixSidedTileFromTheGameboard(die,i)

            ### CONVERT 1 DIE INTO 2 WORKER TILES
            for i in range(0,len(pb.dice)):
                self.actionTakeWorkerTiles(i)

            ### TAKE FROM STORAGE AND PLACE IN ESTATE
            for ndie,die in enumerate(pb.dice):
                for nstorage,tile in enumerate(pb.storage):
                    possibilities = pb.estate.findAvailableTypeDieN(tile.type,die)
                    for nestatetile in possibilities:
                        if tile.type == 'Beige':
                            zone = pb.estate.whichzone(nestatetile)
                            if pb.estate.zoneSubtypeAvailable(tile.subtype,zone) or self.science[1]:
                                self.actionAddSixSidedTileToYourEstate(ndie,nstorage,nestatetile)
#                            else:
#                                print 'Oops! Couldnt place because another city of the same type was already present in zone',zone
                        else:
                            self.actionAddSixSidedTileToYourEstate(ndie,nstorage,nestatetile)
                        

            if self.playerboard.worker > 0 and self.playerboard.worker <= 2:
                for ndie in range(0,len(pb.dice)):
                    self.convertWorker(ndie,+1)
                    self.convertWorker(ndie,-1)
##                    if self.science[8]:
##                        self.convertWorker(ndie,+2)
##                        self.convertWorker(ndie,-2)

            if self.playerboard.silverlingstorage >= 2 and len(self.playerboard.storage) < 3:
                for ndepot in self.gameboard.blackdepot.keys():
                    if not self.gameboard.blackdepot[ndepot] == None:
                        self.actionTakeFromBlackdepot(ndepot)
##                if self.science[6]:

            if not self.sold:
                for ndie,die in enumerate(self.playerboard.dice):
                    p = self.goodsstorposition(self.playerboard.goodsstorage, die)
                    if p >= 0 and p <= 2:
                        self.actionSellGoods(ndie,p)


        else:
            if self.effect.type == 'Dark Green':
                for i in range(1,7):
                    self.effectDarkGreen(i)
            if self.effect.type == 'Beige':
                if self.effect.subtype[0] in ["Carpenter's Workshop", 'Church', 'Market']:
                    self.effectTakeFromGameboard(self.effect.subtype)
                elif self.effect.subtype[0] in ['City Hall']:
                    self.effectPlaceOnEstate()
            self.effect = None

    def effectPlaceOnEstate(self):
        pb = self.playerboard
        ndie = 1
        for nstorage,tile in enumerate(pb.storage):
            for die in range(1,6):
                possibilities = pb.estate.findAvailableTypeDieN(tile.type,die)
                for nestatetile in possibilities:
                    if tile.type == 'Beige':
                        zone = pb.estate.whichzone(nestatetile)
                        if pb.estate.zoneSubtypeAvailable(tile.subtype,zone) or self.science[1]:
                            self.actionAddSixSidedTileToYourEstate(ndie,nstorage,nestatetile,False)
#                        else:
#                            print 'Oops! Couldnt place because another city of the same type was already present in zone',zone
                    else:
                        self.actionAddSixSidedTileToYourEstate(ndie,nstorage,nestatetile,False)
#        print 'effect city hahll'
        self.effect = None

    def effectTakeFromGameboard(self,subtype):
        map = {"Carpenter's Workshop":['Beige'], 'Church':['Grey','Yellow','Dark Green'], 'Market':['Green','Blue'] }
        if subtype[0] in map and len(self.playerboard.storage) < 3:
            for i in range(1,7):
                for k in range(1,5):
                    if not self.gameboard.depots[i][k] == None:
                        if self.gameboard.depots[i][k].type in map[subtype[0]]:
                            self.actionTakeSixSidedTileFromTheGameboard(i,k,False)
        self.effect = None

    ## given l=[[],[],[]], returns the index of the entry of die type, and -1 if it doesn't exist
    def goodsstorposition(self,l,die):
        for index,k in enumerate(l):
            if k:
                if k[0].type == die:
                    return index
        return -1
        
    @log
    def actionSellGoods(self, ndie, pos):
        ''' Use ndie to sell goods in position pos.'''
#        print 'first',self.playerboard.goodsstorage
        points = len(self.playerboard.goodsstorage[pos]) * self.gameboard.nplayers
        self.vp += points
#        print 'VP increment!'

        self.playerboard.silverlingstorage += 1
        if self.verbose:
            print 'Using die',die,' sold goods, won',points,'points and 1 silverling'
        if self.science[3]:
            self.playerboard.silverlingstorage += 1
            if self.verbose:
                print '... and 1 silverling more (science 3)'
        if self.science[4]:
            self.playerboard.worker += 1
            if self.verbose:
                print '... and 1 worker (science 4)'

        self.playerboard.goodsstorage[pos] = []
        die = self.playerboard.dice.pop(ndie)
#        print 'second',self.playerboard.goodsstorage
        self.sold = True


def stratMaxTiles(self, v): ## takes a list of final Player states, and chooses one.
    ### strat starts here....
    ntiles = []
    for i in v:
        ntiles.append(i.playerboard.estate.ntiles())
    maxtiles = max(ntiles)
    maxpos = ntiles.index(maxtiles)
    selected = v[maxpos]
    ### ... and ends here

    self.verbose = True
    for i in selected.called:
        i.call(self)
    self.verbose = False
    self.called = []

def stratMaxTilesRand(self, v): ## takes a list of final Player states, and chooses one.
    ### strat starts here....
    ntiles = []
    for i in v:
        ntiles.append(i.playerboard.estate.ntiles())
    maxtiles = max(ntiles)
    ntiles = []
    for i in v:
        nt = i.playerboard.estate.ntiles()
        if nt == maxtiles:
            ntiles.append(i)
    print 'STRAT:',len(ntiles),'out of',len(v),'with',maxtiles,'tiles'
    selected = ntiles[random.randint(0,len(ntiles)-1)]
    ### ... and ends here

    self.verbose = True
    for i in selected.called:
        i.call(self)
    self.verbose = False
    self.called = []

def stratMaxVP(self, v): ## takes a list of final Player states, and chooses one.
    ### strat starts here....
    vp = []
    for i in v:
        vp.append(i.vp)
    maxvp = max(vp)
    print 'max vp:', maxvp
    maxpos = vp.index(maxvp)
    selected = v[maxvp]
    ### ... and ends here

    self.verbose = True
    for i in selected.called:
        i.call(self)
    self.verbose = False
    self.called = []

def stratRand(self,v):
    l = len(v)
    selected = v[random.randint(0,l-1)]

    self.verbose = True
    for i in selected.called:
        i.call(self)
    self.verbose = False
    self.called = []


def initializeEstate():
    e = [0]
    for i in range(0,37):
        e.append(EstateTile())
    e[1].type = 'Green'
    e[1].die = 6
    e[1].neighbor = [e[2],e[5],e[6]]
    e[1].pos = 0
    e[2].type = 'Dark Green'
    e[2].die = 5
    e[2].neighbor = [e[1],e[3],e[6],e[7]]
    e[2].pos =1
    e[3].type = 'Dark Green'
    e[3].die = 4
    e[3].neighbor = [e[2],e[4],e[7],e[8]]
    e[3].pos =2
    e[4].type = 'Yellow'
    e[4].die = 3
    e[4].neighbor = [e[3],e[8],e[9]]
    e[4].pos =3
    e[5].type = 'Green'
    e[5].die = 2
    e[5].neighbor = [e[1],e[6],e[10],e[11]]
    e[5].pos =4
    e[6].type = 'Green'
    e[6].die = 1
    e[6].neighbor = [e[1],e[2],e[5],e[7],e[11],e[12]]
    e[6].pos =5
    e[7].type = 'Dark Green'
    e[7].die = 6
    e[7].neighbor = [e[2],e[3],e[6],e[8],e[12],e[13]]
    e[7].pos =6
    e[8].type = 'Yellow'
    e[8].die = 5
    e[8].neighbor = [e[3],e[4],e[7],e[9],e[13],e[14]]
    e[8].pos =7
    e[9].type = 'Beige'
    e[9].die = 4
    e[9].neighbor = [e[4],e[8],e[14],e[15]]
    e[9].pos =8
    e[10].type = 'Green'
    e[10].die = 5
    e[10].neighbor = [e[5],e[11],e[16],e[17]]
    e[10].pos =9
    e[11].type = 'Green'
    e[11].die = 4
    e[11].neighbor = [e[5],e[6],e[10],e[12],e[17],e[18]]
    e[11].pos =10
    e[12].type = 'Beige'
    e[12].die = 3
    e[12].neighbor = [e[6],e[7],e[11],e[13],e[18],e[19]]
    e[12].pos =11
    e[13].type = 'Yellow'
    e[13].die = 1
    e[13].neighbor = [e[7],e[8],e[12],e[14],e[19],e[20]]
    e[13].pos =12
    e[14].type = 'Beige'
    e[14].die = 2
    e[14].neighbor = [e[8],e[9],e[13],e[15],e[20],e[21]]
    e[14].pos =13
    e[15].type = 'Beige'
    e[15].die = 3
    e[15].neighbor = [e[9],e[14],e[21],e[22]]
    e[15].pos =14
    e[16].type = 'Blue'
    e[16].die = 6
    e[16].neighbor = [e[10],e[17],e[23]]
    e[16].pos =15
    e[17].type = 'Blue'
    e[17].die = 1
    e[17].neighbor = [e[10],e[11],e[16],e[18],e[23],e[24]]
    e[17].pos =16
    e[18].type = 'Blue'
    e[18].die = 2
    e[18].neighbor = [e[11],e[12],e[17],e[19],e[24],e[25]]
    e[18].pos =17
    e[19].type = 'Dark Green'
    e[19].die = 6
    e[19].neighbor = [e[12],e[13],e[18],e[20],e[25],e[26]]
    e[19].pos =18
    e[20].type = 'Blue'
    e[20].die = 5
    e[20].neighbor = [e[13],e[14],e[19],e[21],e[26],e[27]]
    e[20].pos =19
    e[21].type = 'Blue'
    e[21].die = 4
    e[21].neighbor = [e[14],e[15],e[20],e[22],e[27],e[28]]
    e[21].pos =20
    e[22].type = 'Blue'
    e[22].die = 1
    e[22].neighbor = [e[15],e[21],e[28]]
    e[22].pos =21
    e[23].type = 'Beige'
    e[23].die = 2
    e[23].neighbor = [e[16],e[17],e[24],e[29]]
    e[23].pos =22
    e[24].type = 'Beige'
    e[24].die = 5
    e[24].neighbor = [e[17],e[18],e[23],e[25],e[29],e[30]]
    e[24].pos =23
    e[25].type = 'Grey'
    e[25].die = 4
    e[25].neighbor = [e[18],e[19],e[24],e[26],e[30],e[31]]
    e[25].pos =24
    e[26].type = 'Beige'
    e[26].die = 3
    e[26].neighbor = [e[19],e[20],e[25],e[27],e[31],e[32]]
    e[26].pos =25
    e[27].type = 'Beige'
    e[27].die = 1
    e[27].neighbor = [e[20],e[21],e[26],e[28],e[32],e[33]]
    e[27].pos =26
    e[28].type = 'Green'
    e[28].die = 2
    e[28].neighbor = [e[21],e[22],e[27],e[33]]
    e[28].pos =27
    e[29].type = 'Beige'
    e[29].die = 6
    e[29].neighbor = [e[23],e[24],e[30],e[34]]
    e[29].pos =28
    e[30].type = 'Grey'
    e[30].die = 1
    e[30].neighbor = [e[24],e[25],e[29],e[31],e[34],e[35]]
    e[30].pos =29
    e[31].type = 'Yellow'
    e[31].die = 2
    e[31].neighbor = [e[25],e[26],e[30],e[32],e[35],e[36]]
    e[31].pos =30
    e[32].type = 'Beige'
    e[32].die = 5
    e[32].neighbor = [e[26],e[27],e[31],e[33],e[36],e[37]]
    e[32].pos =31
    e[33].type = 'Grey'
    e[33].die = 6
    e[33].neighbor = [e[27],e[28],e[32],e[37]]
    e[33].pos =32
    e[34].type = 'Grey'
    e[34].die = 3
    e[34].neighbor = [e[29],e[30],e[35]]
    e[34].pos =33
    e[35].type = 'Yellow'
    e[35].die = 4
    e[35].neighbor = [e[30],e[31],e[34],e[36]]
    e[35].pos =34
    e[36].type = 'Yellow'
    e[36].die = 1
    e[36].neighbor = [e[31],e[32],e[35],e[37]]
    e[36].pos =35
    e[37].type = 'Beige'
    e[37].die = 3
    e[37].neighbor = [e[32],e[33],e[36]]
    e[37].pos =36
    e.pop(0)
    return e

def initializeZones(e):
    zone0 = [e[0],e[4],e[5],e[9],e[10]]
    zone1 = [e[1],e[2],e[6]]
    zone2 = [e[3],e[7],e[12]]
    zone3 = [e[8],e[13],e[14]]
    zone4 = [e[11]]
    zone5 = [e[15],e[16],e[17]]
    zone6 = [e[18]]
    zone7 = [e[19],e[20],e[21]]
    zone8 = [e[22],e[23],e[28]]
    zone9 = [e[24],e[29],e[33]]
    zone10 = [e[27]]
    zone11 = [e[25],e[26],e[31],e[32],e[36]]
    zone12 = [e[30],e[34],e[35]]
    return [zone0,zone1,zone2,zone3,zone4,zone5,zone6,zone7,zone8,zone9,zone10,zone11,zone12]

game = Game(2)

game.player[0].strat = stratMaxTilesRand
game.player[1].strat = stratMaxTiles
#print game.player1.playerboard.estate.whichzone(3)
#exit()
print len(game.gameboard.pile['goodstiles'])
game.incturn()
game.incturn()
game.incturn()
game.incturn()
game.incturn()
game.incturn()
game.incturn()
game.incturn()
game.incturn()
game.incturn()
game.incturn()

#print 'number of chickens in zone 0:',game.player1.playerboard.estate.countAnimalsInAZone('Chicken',0)
#print 'number of cows in zone 0:',game.player1.playerboard.estate.countAnimalsInAZone('Cows',0)
#print 'number of pigs in zone 0:',game.player1.playerboard.estate.countAnimalsInAZone('Pigs',0)
#print 'total number of tiles:',game.player1.playerboard.estate.ntiles()
print 'number of VPs:',game.player[0].vp
print 'number of mines:',game.player[0].playerboard.estate.countMines()
print 'number of silverlings:',game.player[0].playerboard.silverlingstorage
print 'avail:',game.player[0].playerboard.estate.zoneSubtypeAvailable('Bank',3)
print 'avail:',game.player[0].playerboard.estate.zoneSubtypeAvailable('Bank',4)
print 'avail:',game.player[0].playerboard.estate.zoneSubtypeAvailable('Bank',8)
print 'avail:',game.player[0].playerboard.estate.zoneSubtypeAvailable('Bank',10)
print 'total number of tiles:',game.player[0].playerboard.estate.ntiles()
exit()

gb = Gameboard(2)
player1 = Player(1,gb)
player1.strat = stratMaxTiles
gb.incturn()

for k in range(0,5):
    player1.roll()

    logandexecute = False
    l = player1.explore()
    player1.strat(player1,l)


print 'player1 ntiles:',player1.playerboard.estate.ntiles()




