import pippy, pygame, sys, math

from pygame.locals import *

from random import *

################################################################################

#Start of external classes and functions

###############################################################################





  ########################################################################

  #Dungeon class:  stores a 2d array of rooms representing the dungeon

  #                reads/parses a text file containing the data for a dungeon

  #######################################################################3

class Dungeon:

  def __init__(self,sizeX=5,sizeY=5,fileName="dungeon2.txt"):

    self.sizeX=sizeX

    self.sizeY=sizeY

    self.fileName=fileName

    ###INITALIZE DICTIONARY, TUPLE:ROOM PAIRINGS

    self.rooms={}

  def fill(self):

    #####open text file######

    dgnFile=open(self.fileName,'r')

    currentX=0

    currentY=0

    for line in dgnFile:

      ###print line for testing###



      ###initialize room variables###

      doorN=False

      doorS=False

      doorE=False

      doorW=False

      shop=False

      en1=0

      en2=0

      en3=0

      en4=0

      ###check characters in current line, set variables accordingly###

      ###KEY:1st character=door to north

      ###    2nd=door to south

      ###    3rd=door to east

      ###    4th=door to west

      ###    5th=if the room is a shop

      ###    6-9=enemy number in each slot (0 for no enemy)

      if line[0]=='N':

        doorN=True

      if line[1]=='S':

        doorS=True

      if line[2]=='E':

        doorE=True

      if line[3]=='W':

        doorW=True

      if line[4]=='S':

        shop=True

      rm=Room(doorN,doorS,doorE,doorW,shop,line[5],line[6],line[7],line[8])

      #print(rm.getData())

      #print(repr(currentX)+", "+repr(currentY))

      self.rooms[(currentX,currentY)]=rm

      ###update position in array###

      currentX+=1

      if currentX==self.sizeX:

        currentY+=1

        currentX=0

      if currentY>self.sizeY:

        break

      

      

##################################################################################

#Room class: stores data about a room in the dungeon.  IE doors, enemies, mood etc

####################################################################################

class Room:

  def __init__(self,doorN=False,doorS=False,doorE=False,doorW=False,shop=False,en1=0,en2=0,en3=0,en4=0):

    self.doorN=doorN

    self.doorS=doorS

    self.doorE=doorE

    self.doorW=doorW

    self.shop=shop

    self.en1=en1

    self.en2=en2

    self.en3=en3

    self.en4=en4

    self.image=0

  #######To string method########

  def getData(self):

    string=""

    string+=repr(self.doorN)+repr(self.doorS)+repr(self.doorE)+repr(self.doorW)

    string+=self.en1+self.en2+self.en3+self.en4

    return(string)

  def setImage(self,imagePath):

    self.image=pygame.image.load(imagePath)





#################################################################################

  #Map class: stores information about the layout of the dungeon for easy display

###############################################################################

class Map:

  def __init__(self,dgn=Dungeon(0,0,'')):

    self.sizeX=dgn.sizeX

    self.sizeY=dgn.sizeY

    self.rectSizeX=38

    self.rectSizeY=38

    self.rects={}

    self.fullRooms={}

    self.totalSurface=pygame.Surface((self.sizeX*40,self.sizeY*40))

    for y in range(self.sizeY):

      for x in range(self.sizeX):

        curRect=pygame.Rect(x*40,y*40,self.rectSizeX,self.rectSizeX)

        self.rects[(x,y)]=curRect

        if dgn.rooms.get((x,y)).doorN:

          self.fullRooms[(x,y)]=True

          print(repr(x)+", "+repr(y)+" True")

          self.totalSurface.fill((255,255,255),curRect,0)

        elif dgn.rooms.get((x,y)).doorS:

          self.fullRooms[(x,y)]=True

          print(repr(x)+", "+repr(y)+" True")

          self.totalSurface.fill((255,255,255),curRect,0)

        elif dgn.rooms.get((x,y)).doorE:

          self.fullRooms[(x,y)]=True

          print(repr(x)+", "+repr(y)+" True")

          self.totalSurface.fill((255,255,255),curRect,0)

        elif dgn.rooms.get((x,y)).doorW:

          self.fullRooms[(x,y)]=True

          print(repr(x)+", "+repr(y)+" True")

          self.totalSurface.fill((255,255,255),curRect,0)

  def display(self,player,screen):

    

    mapView=pygame.transform.chop(self.totalSurface,(0,0,0,0))

    mapView.fill((255,0,0),(player.currentX*40,player.currentY*40,38,38))

    NORTH=1

    SOUTH=3

    EAST=0

    WEST=2

    angle=0



    if player.playerFacing==NORTH:

      angle=0

      mapView=pygame.transform.rotate(mapView,angle)

      angle=90

    elif player.playerFacing==SOUTH:

      angle=180

      mapView=pygame.transform.rotate(mapView,angle)

      angle=270

    elif player.playerFacing==EAST:

      angle=90

      mapView=pygame.transform.rotate(mapView,angle)

      angle=0

    elif player.playerFacing==WEST:

      angle=270

      mapView=pygame.transform.rotate(mapView,angle)

      angle=180

    angle=angle*(math.pi/180)

    



    curSect=pygame.Rect(0,700,200,200)



    curSect.top+=((player.currentX*40-81)*math.cos(angle))-((player.currentY*40-81)*math.sin(angle))



    curSect.left-=((player.currentX*40-81)*math.sin(angle))+((player.currentY*40-81)*math.cos(angle))



    screen.fill(0,(0,700,200,300),0)

    screen.blit(mapView,curSect)

    screen.fill(0,(200,700,1200,300),0)

        



###########################################################################

#  Menu class:  contains a list of options (which can be other menus)

#               has a background image as well as images for each option

###########################################################################

class Menu:

    def __init__(self,options,player,bgImageFile,optionImageFiles,name):

        self.options=options

        self.currentOption=0

        self.background=pygame.sprite.Sprite()

        self.background.image=pygame.image.load(bgImageFile)

        self.background.rect=pygame.Rect(0,0,1290,900)

        self.optionsImages=[]

        i=0

        for name in optionImageFiles:

            sprite=pygame.sprite.Sprite()

            sprite.image=pygame.image.load(name)

            sprite.rectangle=pygame.Rect(0,0,1290,60)

            self.optionsImages.append(sprite)

            i+=1

        self.size=i

    def draw(self,player,screen,xStart,yStart,height):
        #if player.battle==False:

        #  player.currentRoomGroup.empty()
        menuGroup=pygame.sprite.Group()

        i=0

        for image in self.optionsImages:

            if i==self.currentOption:

                image.rect=pygame.Rect(xStart+30,yStart+(i*height),1290,height)

            else:

                image.rect=pygame.Rect(xStart,yStart+(i*height),1290,height)

            menuGroup.add(image)

            i+=1

        bgGroup=pygame.sprite.Group(self.background)

        bgGroup.draw(screen)

        menuGroup.draw(screen)
        if player.battle==False:

          pygame.display.flip()

    def select(self,direction):

        if direction=="up":

            if self.currentOption>0:

                self.currentOption-=1

            else:

                self.currentOption=0

        else:

            if self.currentOption<self.size:

                self.currentOption+=1

            else:

                self.currentOption=self.size

    def progress(self,player,screen):

        if type(self.options[self.currentOption])==type(self):

            player.currentMenu=self.options[self.currentOption]

            player.previousMenu=self

        else:

            self.updateByName(self.options[self.currentOption],player,screen)

    def regress(self,player):

        temp=player.currentMenu

        player.currentMenu=player.previousMenu

        player.previousMenu=temp

    def updateByName(self,name,player,screen):

        if name=="New Game":

            player.traversal=True

            player.mainMenu=False

            setImage(player)
            player.battlePlayer=Hero(player)
            player.currentRoom=player.dgn.rooms.get((0,0))

            player.currentRoomGroup.draw(screen)

            pygame.display.flip()

        elif name=="Close":

            sys.exit()

        elif name=="Tutorial":

            player.inTutorial=True
            player.mainMenu=False

        elif name=="Attack":

            player.curBattle.attack(player.battlePlayer,"basic")

        elif name=="Do Nothing":
          player.curBattle.doNothing()   

        #WILL ADD MORE OPTIONS LATER

		# LATER IS NOW - Preston 11-7-09

			

	elif name=="Attack":

	    player.traversal = False

	    player.battle = True

	    optArr = ["0","1","2","3","4","5","6","7","8","9"]

	    Menu(optArr,

"/home/olpc/images/numPadbackground.gif",["/home/olpc/images/0.gif","/home/olpc/images/1.gif","/home/olpc/images/2.gif","/home/olpc/images/3.gif","/home/olpc/images/4.gif","/home/olpc/images/5.gif","/home/olpc/images/6.gif","/home/olpc/images/7.gif","/home/olpc/images/8.gif","/home/olpc/images/9.gif"],"Number Pad")

	    optArr.draw(player.currentRoomGroup,screen,400,300,200)

	else:

	    sys.exit()

######################################################################

#Tutorial Class: stores image list, traverses through list

######################################################################

class Tutorial:

    def __init__(self,imageList):

        self.currentIndex = 0

        self.images=[]

        for image in imageList:

            spt=pygame.sprite.Sprite()

            spt.image=pygame.image.load(image)

            spt.rect=pygame.Rect(0,0,1290,700)

	    

	    self.images.append(spt)

      

       	self.size=len(imageList)

    def next(self):

	

    	if  self.currentIndex < self.size - 1:

       	 	self.currentIndex+=1

    	else:
                self.currentIndex=0

		player.mainMenu = True

		player.inTutorial = False



    def previous(self):
      if self.currentIndex > 0:

        self.currentIndex-=1
      else:
        self.currentIndex=0

    def draw(self,group,screen):

        group.empty()

        group.add(self.images[self.currentIndex])

        group.draw(screen)

        pygame.display.flip()

            

################################################################################

# Player Class: stores info about the player ie. current position in dungeon etc

#########################################################################

class Player:

  ####LOADS EVERYTHING FOR THE GAME####

  def __init__(self,x=0,y=0):

    NORTH=1

    SOUTH=3

    EAST=0

    WEST=2



    self.initializeMenu()

    self.loadTutorial()

    self.loadImages()

    self.battlePlayer=Hero(self)

    self.curBattle=BattleEngine(self.battlePlayer,["Goblin"])

    #state variables

    self.inTutorial=False

    self.mainMenu=True

    self.traversal=False

    self.waiting=False

    self.battle=False

    self.statMenu=False

    
    self.msg1=""
    self.msg2=""
    self.msg3=""
    self.msg4=""
    self.msg5=""

    #traversal variables

    self.currentX=x

    self.currentY=y

    self.dgn=Dungeon(5,5,"/home/olpc/images/dungeon2.txt")

    self.dgn.fill()

    #self.currentRoom=Room(False,False,False,False,False,0,0,0,0)

    self.currentRoom=self.dgn.rooms.get((self.currentX,self.currentY))

    self.dgnMap=Map(self.dgn)



    self.currentRoom=self.dgn.rooms.get((self.currentX,self.currentY))

    self.playerFacing=SOUTH



    #sound

    self.doorEffect=pygame.mixer.Sound("/home/olpc/images/door.wav")

  def initializeMenu(self):

    mainMenuImages=["/home/olpc/images/TutorialButton.gif","/home/olpc/images/NewGameButton.gif","/home/olpc/images/CloseButton.gif"]

    self.MainMenu=Menu(["Tutorial","New Game","Close"],self,"/home/olpc/images/TitleImage.gif",mainMenuImages,"Main Menu")

    self.currentMenu=self.MainMenu
    self.previousMenu=self.MainMenu

  def loadTutorial(self):

    tutorialImages=["/home/olpc/images/t1.gif","/home/olpc/images/t2.gif","/home/olpc/images/t3.gif"]

    self.tutorial=Tutorial(tutorialImages)

  def loadImages(self):

    self.currentRoomSprite=pygame.sprite.Sprite()

    self.currentRoomSprite.image=pygame.image.load("/home/olpc/images/beyond_zork.jpg")

    self.currentRoomSprite.rect=pygame.Rect(0,0,1200,700)



    self.Black=pygame.sprite.Sprite()

    self.Black.image=pygame.image.load("/home/olpc/images/Black.gif")

    self.Black.rect=pygame.Rect(0,0,1200,700)



    self.FLRSprite=pygame.sprite.Sprite()

    self.FLRSprite.image=pygame.image.load("/home/olpc/images/flr.gif")

    self.FLRSprite.rect=self.currentRoomSprite.rect



    self.FRSprite=pygame.sprite.Sprite()

    self.FRSprite.image=pygame.image.load("/home/olpc/images/fr.gif")

    self.FRSprite.rect=self.currentRoomSprite.rect



    self.FSprite=pygame.sprite.Sprite()

    self.FSprite.image=pygame.image.load("/home/olpc/images/f.gif")

    self.FSprite.rect=self.currentRoomSprite.rect



    self.FLSprite=pygame.sprite.Sprite()

    self.FLSprite.image=pygame.image.load("/home/olpc/images/fl.gif")

    self.FLSprite.rect=self.currentRoomSprite.rect



    self.LRSprite=pygame.sprite.Sprite()

    self.LRSprite.image=pygame.image.load("/home/olpc/images/lr.gif")

    self.LRSprite.rect=self.currentRoomSprite.rect



    self.LSprite=pygame.sprite.Sprite()

    self.LSprite.image=pygame.image.load("/home/olpc/images/l.gif")

    self.LSprite.rect=self.currentRoomSprite.rect



    self.NoSprite=pygame.sprite.Sprite()

    self.NoSprite.image=pygame.image.load("/home/olpc/images/_.gif")

    self.NoSprite.rect=self.currentRoomSprite.rect



    self.RSprite=pygame.sprite.Sprite()

    self.RSprite.image=pygame.image.load("/home/olpc/images/r.gif")

    self.RSprite.rect=self.currentRoomSprite.rect



    self.currentRoomGroup=pygame.sprite.Group(self.currentRoomSprite)



#######################################################################

#Hero class - represents the player in battle and holds all of their data

##########################################################################

class Hero:
  def __init__(self,player):

#****property********value**********************description**********************#

	self.MHP 	= 40		#maximum health points (base HP)

	self.HP		= 40		#current health points

	self.BHP 	= 0		#bonus health points (from equipment)

	self.ATT 	= 10		#base attack power

	self.BAB	= 0		#bonus attack power (from battle timer)

	self.BAE	= 0		#bonus attack power (from equipment)

	self.DEF	= 1		#base defense power

	self.BDE	= 0		#bonus defense  power(from equipment)

	self.eqItems_Ar	= []	#equipped items

	self.inv_Ar 	= []	#inventory

	self.attacks_Ar = []	#associated array for attack string names and attack power values



	self.inv_Ar = []

	self.attacks_Ar = []

	

#****HERO ACCESSORS*********************************************#

	#returns player's maximum health

  def maxHealthPoints(self):

    return (self.HP + self.BHP)

	

	#returns player's current health

  def healthPoints(self):

    return (self.HP)

	

	#returns player's current attack power

  def attackPower(self,name):

    if name=="basic":

      return self.ATT+self.BAB+self.BAE

	

	#returns player's current defense power
  def defensePower(self):

    return (self.DEF + self.BDE)

		

	#returns player's equipped items

  def equipment(self):

    return self.eqItems_Ar

	

	#returns player's current inventory

  def inventory(self):

    return self.inv_Ar

		

#****HERO MUTATORS************************************************#

	#sets player's current health

  def setHealth(self,_HP):

    self.HP = _HP

		

	#sets player's bonus health

  def setBonusHP(self,_BHP):

    self.BHP = _BHP

		

	#sets player's bonus attack power (from battle timer)

  def setBonusAP(self,_BAP):

    self.BAP = _BAP

		

	#sets player's bonus attack power (from equipment)

  def setBonusAE(self,_BAE):

    self.BAE = _BAE

	

	#sets player's bonus defense power (from equipment)

  def setBonusDE(self,_BDE):

    self.BDE = _BDE

		

	#increases player's current health by given amount

  def giveHealth(self,_inc):

    self.HP += _inc

		

    if healthPoints() > maxHealthPoints():

	setHealth(maxHealthPoints())

	

	#player is attacked by given damage

  def defendAttack(self,dmg):

    self.HP -= (dmg - self.defensePower())



#****BATTLE ACCESSORS***********************************************#

	#returns player's list of attacks that are currently available for use

  def availableAttacks(self):

    return self.attacks_Ar

	#returns the attack power of a given attack type

	

#****INVENTORY MUTATORS********************************************#

	#add item to equipment

  def addEquipment(self,_item):

		#add  _item to equipment

    if _item.getType() is "WEAPON":

      eqItem_Ar[0] = _item

    elif _item.getType() is "ARMOR":

      eqItem_Ar[1] = _item

    else:

      for i in range(2,5):
        print(i)  # go through the rest of the equipped items, trade out values

			#look through last 4 slots, find empty cell and add. Otherwise you must unequip an item first to have an empty cell

			

		#alternative

			#depending on item type - only give access to certain cells. So, if item is WEAP, only allow equip on slot 0, if item is ARM, only allow equip on slot1, if item is ITEM, only allow equip on slots2-5, whatever slot is picked -trade values (unequip item and equip new)

		

	#remove item from equipment

  def remEquipment(self,_item):
    print("equipement removed")
          #remove _item from equipment -- leave cell empty

	#add item to inventory

  def addInventory(self,_item):

    print("item added")
          #add _item to end of inventory

  def remInventory(self,_item):
    print("item dropped")
          #remove _item from inventory

#end class Hero

		

##############################################################################		

#Enemy class - represents an enemy and holds all of its data

#############################################################

class Enemy:
  def __init__(self):

#****property********value**********************description**********************#

	self.MHP 	= 40				#maximum health points (base HP)

	self.HP		= 40				#current health points

	self.BHP 	= 0				#bonus health points (from equipment)

	self.ATT 	= 10 				#base attack power

	self.BAE	= 0				#bonus attack power (from equipment)

	self.DEF	= 1				#base defense power

	self.BDE	= 0				#bonus defense  power(from equipment)

	self.eqItems_Ar	= []	#equipped items

	self.attacks_Ar = []	#associated array for attack string names and attack power values

	

	self.eqItem_Ar = []

	self.inv_Ar = []

	self.attacks_Ar = []
        self.sprite=pygame.sprite.Sprite()
        #load image based on type later
        self.sprite.image=pygame.image.load("/home/olpc/images/concept_wizard.gif")
        self.sprite.rect=(200,200,50,300) 

	

#****ENEMY ACCESSORS*********************************************#

	#returns enemy's maximum health

  def maxHealthPoints(self):

    return (self.HP + self.BHP)

	

	#returns enemy's current health

  def healthPoints(self):

    return (self.HP)

	

	#returns enemy's current attack power

  def attackPower(self):

    return (self.ATT + self.BAP + self.BAE)

	

	#returns enemy's current defense power

  def defensePower(self):

    return (self.DEF + self.BDE)

		

	#returns enemy's equipped items

  def equipment(self):

    return self.eqItems_Ar

	

	#returns enemy's current inventory

  def inventory(self):

    return self.inv_Ar

		

#****ENEMY MUTATORS************************************************#

	#sets enemy's current health

  def setHealth(self,_HP):

    self.HP = _HP

		

	#sets enemy's bonus health

  def setBonusHP(self,_BHP):

    self.BHP = _BHP

		

	#sets enemy's bonus attack power (from battle timer)

  def setBonusAP(self,_BAP):

    self.BAP = _BAP

		

	#sets enemy's bonus attack power (from equipment)

  def setBonusAE(self,_BAE):

    self.BAE = _BAE

	

	#sets enemy's bonus defense power (from equipment)

  def setBonusDE(self,_BDE):

    self.BDE = _BDE

		

	#increases enemy's current health by given amount

  def giveHealth(self,_inc):

    self.HP += _inc

		

    if healthPoints(self) > maxHealthPoints(self):

	setHealth(self,maxHealthPoints(self))

	

	#enemy is attacked by given damage

  def defendAttack(self,dmg):

    self.HP -= (dmg - self.defensePower())

		

#****BATTLE ACCESSORS***********************************************#

	#returns player's list of attacks that are currently available for use

  def availableAttacks(self):

    return self.attacks_Ar

		

#****INVENTORY MUTATORS********************************************#

	#add item to equipment

  def addEquipment(self,_item):
    print("add equip")

		#add  _item to equipment

		#if _item is weapon - add to first slot

		#if _item is armor - add to second slot

		#if _item is consumable - add to slots 3-6

		

	#remove item from equipment

  def remEquipment(self,_item):
    print("remove equip")

		#remove _item from equipment -- leave cell empty

	

#end class Enemy







###################################################################

# Begin Battle Engine Class

################################################################



class BattleEngine:

  def __init__(self,player,enemyArr):

	#Bool if it is the players turn or not

	self.playerTurn = True

	

	#Index that tracks which enemy is up to attack

	self.enemyTurnIndex = 0



	###

	# Basic constructor, takes in the player and a group of enemies

	###


	self.player = player

	self.enemies = enemyArr

	self.t = 0

	self.tTracker = 0

	self.maxBonusTime = 0
        self.initializeMenus()
        self.selEnemyIndex=0

	self.player.msg5= "Enemies are present, prepare to fight."
  def initializeMenus(self):
    battleOptions=["Attack","Do Nothing"]
    battleBackground="/home/olpc/images/battleMenubackground.gif"
    battleOptImg=["/home/olpc/images/attackButton.gif","/home/olpc/images/nothing.gif"]
    
    self.battleMenu=Menu(battleOptions,self.player,battleBackground,battleOptImg,"Battle")
    self.battleMenu.background.rect=(200,580,200,200)
    self.battleMenu.size=1
    #self.numPad=Menu()
    self.player.currentMenu=self.battleMenu

  def draw(self,player,screen):

            #draw enemies

            x=50

            y=150
            enemyGroup=pygame.sprite.Group()

            for enemy in self.enemies:

                x+=200

                enemy.sprite.rect=(x,y,200,200)
                enemyGroup.add(enemy.sprite)

                
            player.currentRoomGroup.draw(screen)
            enemyGroup.draw(screen)

            #draw player

            player.currentMenu.draw(player,screen,200,580,60)

            pygame.display.flip()

            

	###

	# Attack function. Takes in the attacker, 

	# name of the attack, and trhe defender

	# Subtractgs the damage from defenders 

	# health based off of how much power the attack has.

	###
  def doNothing(self):
    self.playerTurn=False

  def attack(self,attacker,attackName):

		attacker.setBonusAP(self.maxBonusTime)

		defender=self.enemies[self.selEnemyIndex]

		defender.defendAttack(attacker.attackPower(attackName))
                print("Player Attack")
                print("Enemy HP:")
                print(defender.HP)
                player.msg1=player.msg2

      		player.msg2=player.msg3

      		player.msg3=player.msg4

      		player.msg4=player.msg5

                player.msg5="You attack for "+repr(attacker.ATT+attacker.BAP)+" damage"
                player.msg1=player.msg2

      		player.msg2=player.msg3

      		player.msg3=player.msg4

      		player.msg4=player.msg5
                player.msg5="Enemy HP is "+repr(defender.HP)

                self.playerTurn=False

		

	###

	#Returns a list of attacks for any player or enemy passed in

	###

  def ListAttacks(self,char):

		return char.avaliableAttacks()

	

	###

	# Keeps track of the Bonus Timer, 

	# takes in how long the timer should run

	###

  def BonusTimer(self,timeLength):

		print timeLength



		#Create and Start Timer

				

		self.t = Timer(timeLength,TimerExpire)

		self.t.start()

		self.maxBonusTime = timeLength

		self.tTracker = Timer(1,trackerExpires)

		

		#Update GUI Timer Bar

	

	###

	# Tracks how long the bonus timer has been running

	###

  def trackerExpires(self):

		self.maxBonusTime = self.maxBonusTime - 1

	

	###

	#

	###

  def TimerEpxire(self):

		print "The bonus time is up"

		

		#Change timer GUI bar color????

	

	

	###

	#Picks an attack for the enemy to perform. 

	# takes in which enemy is attacking.

	###

  def GenerateEnemyAttack(self,enemy):

	  #AvalAttacks = ListAttacks(enemy)
          enemy.setBonusAP(self.maxBonusTime)

	  defender=self.player.battlePlayer

	  defender.defendAttack(enemy.attackPower())
          self.playerTurn=True
          print("Enemy Attack")
          print("Player HP")
          print(self.player.battlePlayer.HP)
	  player.msg1=player.msg2

      	  player.msg2=player.msg3

      	  player.msg3=player.msg4

      	  player.msg4=player.msg5

          player.msg5="Enemy attacks for "+repr(enemy.ATT+enemy.BAP)+" damage"
          player.msg1=player.msg2

          player.msg2=player.msg3

      	  player.msg3=player.msg4

      	  player.msg4=player.msg5
          player.msg5="Your HP is "+repr(defender.HP)

		#Fill in AI logic here to pick an attack, for now Math.random

	  #return AvalAttacks(random.randrange((len(AvalAttacks)-1)))

		

	###

	#Called when battle is over and player wins

	###

  def Victory(self):

    #self.player.winScreen(self)

    self.player.battle=False
    self.player.traversal=True
    self.player.msg5="You Win!"

    #self.player.winScreen=True



		#Return to travesal system

	

	###

	#Called when battle is over and player loses

	###

  def Defeat(self):

    #self.player.defeatScreen=True

    self.player.battle=False
    self.player.currentMenu=self.player.MainMenu

    self.player.mainMenu=True	

		#end the game

		

	###

	#Checks if the battle is over

	###

  def CheckEndBattle(self):

    if player.battlePlayer.HP < 0:

      self.Defeat()

    else:

	allDead = True

	for enem in self.enemies:

	    if enem.HP > 0:

	      allDead = False

	      break

			

	if allDead == True:

          self.Victory()

	

	###

	# Run updates the battle and keeps things progressing

	###

  def Run(self,event,screen):

    print("Run Method")

		#Insert logic that updates the battle here

		

		#If player turn, wait for player to select attack then start timer

    if self.playerTurn==True:

      if event.type == QUIT:

        sys.exit()

                    #handle key input

      elif event.type == KEYDOWN:

        newKey=pygame.key.name(event.key)

        if newKey=='escape':

          sys.exit()

        elif newKey=='[1]':

          #Right

          player.currentMenu.progress(player,screen)

        elif newKey=='[2]':

          #Down

          player.currentMenu.select("down")

        elif newKey=='[3]':

          #Left

          player.currentMenu.regress(player)

        elif newKey=='[8]':

          #Up

          player.currentMenu.select("up")

        elif newKey=='[4]':

          #Left

          print(newKey)

        elif newKey=='[5]':

          #X

          player.currentMenu.regress(player)

        elif newKey=='[6]':

          #Check

          player.currentMenu.progress(player,screen)

        elif newKey=='[7]':

          #Square

          msg5='square'

        elif newKey=='[9]':

          msg5='circle'

    else: 
      self.GenerateEnemyAttack(self.enemies[self.selEnemyIndex])

		# if enemy turn, randomly select enemy attack using GenerateEnemeyAttack() and attack

		

		#Run a check to see if battle is over
    self.CheckEndBattle()

	###

	# Uses an item

	###

  def useItem(self,inventoryID):

		#Access players inventory and use the selected item

		

		#Add Health or do damage according to the items description

		

		#Delete Item From Inventory

		

		#Resume
    self.Run()

	

		

#############################################################################

#End External Classes

######################################################################









            

# always need to init first thing

pygame.init()





# turn off cursor

pygame.mouse.set_visible(False)



# XO screen is 1200x900

size = width, height = 1200, 900



# we'll use 36 pixel high text

fsize = 36





# create the window and keep track of the surface

# for drawing into

screen = pygame.display.set_mode(size)



# create a Font object from a file, or use the default

# font if the file name is None. size param is height

# in pixels



font = pygame.font.Font(None, fsize)


player=Player(0,0)



#state variables

player.inTutorial=False

player.traversal=False

player.waiting=False

player.battle=False

player.mainMenu=True

player.statMenu=False

# Font.render draws text onto a new surface.

#

# usage: Font.render(text, antialias, color, bg=None)

tl1=font.render(player.msg1,True,(255,255,255))

tl2=font.render(player.msg2,True,(255,255,255))

tl3=font.render(player.msg3,True,(255,255,255))

tl4=font.render(player.msg4,True,(255,255,255))

tl5=font.render(player.msg5,True,(255,255,255))



# the Rect object is used for positioning

bigRect = pygame.Rect(300,700,800,200)

#textRect=text.get_rect()

line1=pygame.Rect(300,700,800,36)

line2=pygame.Rect(300,736,800,36)

line3=pygame.Rect(300,772,800,36)

line4=pygame.Rect(300,808,800,36)

line5=pygame.Rect(300,844,800,36)



# start at the top left

bigRect.left = 300

bigRect.top = 700

bigRect.width=1000

bigRect.height=300



#####Functions for main class######

def enterRoom(direction,player,screen):

    NORTH=1

    SOUTH=3

    EAST=0

    WEST=2

    

    if direction=='north':

        player.currentY-=1

        player.playerFacing=NORTH

    elif direction=='south':

        player.currentY+=1

        player.playerFacing=SOUTH

    elif direction=='east':

        player.currentX+=1

        player.playerFacing=EAST

    elif direction=='west':

        player.currentX-=1

        player.playerFacing=WEST

    else:

        print(direction)

    player.currentRoom=player.dgn.rooms.get((player.currentX,player.currentY))



    player.doorEffect.play()



    player.currentRoomGroup.remove(player.currentRoomSprite)

    player.currentRoomSprite=player.Black

    player.currentRoomGroup.add(player.currentRoomSprite)

    player.currentRoomGroup.draw(screen)

    player.waiting=True

    #player.traversal=False

    

    #setImage(player)

    return("You enter room at "+repr(player.currentX)+", "+repr(player.currentY))



def setImage(player):

    fileName=""

    NORTH=1

    SOUTH=3

    EAST=0

    WEST=2

    ###Set up string for testing

    if player.playerFacing==NORTH:

        if player.currentRoom.doorN:

            fileName+="F"

        if player.currentRoom.doorW:

            fileName+="L"

        if player.currentRoom.doorE:

            fileName+="R"

    elif player.playerFacing==SOUTH:

        if player.currentRoom.doorS:

            fileName+="F"

        if player.currentRoom.doorE:

            fileName+="L"

        if player.currentRoom.doorW:

            fileName+="R"

    elif player.playerFacing==EAST:

        if player.currentRoom.doorE:

            fileName+="F"

        if player.currentRoom.doorN:

            fileName+="L"

        if player.currentRoom.doorS:

            fileName+="R"

        

    elif player.playerFacing==WEST:

        if player.currentRoom.doorW:

            fileName+="F"

        if player.currentRoom.doorS:

            fileName+="L"

        if player.currentRoom.doorN:

            fileName+="R"

    ###set sprite depending on string

    player.currentRoomGroup.empty()

    if fileName=="F":

        player.currentRoomSprite=player.FSprite

    elif fileName=="FL":

        player.currentRoomSprite=player.FLSprite

    elif fileName=="FR":

        player.currentRoomSprite=player.FRSprite

    elif fileName=="FLR":

        player.currentRoomSprite=player.FLRSprite

    elif fileName=="LR":

        player.currentRoomSprite=player.LRSprite

    elif fileName=="L":

        player.currentRoomSprite=player.LSprite

    elif fileName=="R":

        player.currentRoomSprite=player.RSprite

    else:

        player.currentRoomSprite=player.NoSprite

    player.currentRoomGroup.add(player.currentRoomSprite)



    

def checkDoor(direction,player,screen):

    NORTH=1

    SOUTH=3

    EAST=0

    WEST=2

    currentX=player.currentX

    currentY=player.currentY

    playerFacing=player.playerFacing

    currentRoom=player.currentRoom

    if direction=='down': 

         print("down pressed")

    elif direction=='up':

         if playerFacing==NORTH:

            if currentRoom.doorN:

                return(enterRoom('north',player,screen))

            else:

                return("There is no door in front of you")

         elif playerFacing==SOUTH:

            if currentRoom.doorS:

                return(enterRoom('south',player,screen))

            else:

                return("There is no door in front of you")

         elif playerFacing==EAST:

            if currentRoom.doorE:

                return(enterRoom('east',player,screen))

            else:

                return("There is no door in front of you")

         elif playerFacing==WEST:

            if currentRoom.doorW:

                return(enterRoom('west',player,screen))

            else:

                return("There is no door in front of you")

                

    elif direction=='left':

        if playerFacing==NORTH:

            player.playerFacing=WEST

            #setImage(player)

            return('You are now facing West')

        elif playerFacing==SOUTH:

            player.playerFacing=EAST

            #setImage(player)

            return('You are now facing East')

        elif playerFacing==EAST:

            player.playerFacing=NORTH

            #setImage(player)

            return('You are now facing North')

        elif playerFacing==WEST:

            player.playerFacing=SOUTH

            #setImage(player)

            return('You are now facing South')

    elif direction=='right':

        if playerFacing==NORTH:

            player.playerFacing=EAST

            #setImage(player)

            return('You are now facing East')

        elif playerFacing==SOUTH:



            player.playerFacing=WEST

            #setImage(player)

            return('You are now facing West')

        elif playerFacing==EAST:

            player.playerFacing=SOUTH

            setImage(player)

            return('You are now facing South')

        elif playerFacing==WEST:

            player.playerFacing=NORTH

            #setImage(player)

            return('You are now facing North')

    else:

        print(direction)



###Update methods###

def updateMenu(event,player):

    menu=player.currentMenu

    if event.type == QUIT:

      sys.exit()



    elif event.type == KEYDOWN:

      newKey=pygame.key.name(event.key)

      if newKey=='escape':

        sys.exit()

      elif newKey=='[1]':

        menu.progress(player,screen)

      elif newKey=='[2]':

        menu.select("down")

      elif newKey=='[3]':

        menu.regress(player)

      elif newKey=='[4]':

        print("left")

      elif newKey=='[5]':

        print('check')

      elif newKey=='[6]':

        print('right')

      elif newKey=='[7]':

        print('square')

      elif newKey=='[8]':

        menu.select("up")

      elif newKey=='[9]':

        print('circle')



def updateTraversal(event,player,screen):

    if event.type == QUIT:

      sys.exit()



    elif event.type == KEYDOWN:

      newKey=pygame.key.name(event.key)

      player.msg1=player.msg2

      player.msg2=player.msg3

      player.msg3=player.msg4

      player.msg4=player.msg5

      if newKey=='escape':

        sys.exit()

      elif newKey=='[1]':

        player.msg5='not implemented'

      elif newKey=='[2]':

        player.msg5=checkDoor('down',player,screen)

      elif newKey=='[3]':

        player.msg5='initiating battle...'
        player.traversal=False
        player.battle=True
        enemyList=[Enemy()]
        player.curBattle=BattleEngine(player,enemyList)

		#ENTER BATTLE MODE ENTRACNE LOGIC

		# FOR NOW JUST CREATE A MENU WITH AN ATTACK OPTION ON IT THEN LEAD UP WITH A NUMBER PAD

		#(self,options,player,bgImageFile,optionImageFiles,name):

	#batMen = Menu(["Attack"],player,

#"/home/olpc/images/battleMenubackground.gif",

##["/home/olpc/images/attackButton.gif"],"Main Battle Menu")

#	batMen.draw(player.currentRoomGroup,screen,400,300,200)

      elif newKey=='[4]':

        player.msg5=checkDoor('left',player,screen)

      elif newKey=='[5]':

        player.msg5='check'

      elif newKey=='[6]':

        player.msg5=checkDoor('right',player,screen)

      elif newKey=='[7]':

        player.msg5='square'

      elif newKey=='[8]':

        player.msg5=checkDoor('up',player,screen)

      elif newKey=='[9]':

        player.msg5='circle'

def updateTutorial(event,player):

    if event.type == QUIT:

      sys.exit()



    elif event.type == KEYDOWN:

      newKey=pygame.key.name(event.key)

      if newKey=='escape':

        sys.exit()

      elif newKey=='[1]':

        player.tutorial.next()

      elif newKey=='[2]':

        player.msg5='down'

      elif newKey=='[3]':

        player.tutorial.previous()

      elif newKey=='[4]':

        player.tutorial.previous()

      elif newKey=='[5]':

        player.msg5='check'

      elif newKey=='[6]':

        player.tutorial.next()

      elif newKey=='[7]':

        player.msg5='square'

      elif newKey=='[8]':

        player.msg5='up'

      elif newKey=='[9]':

        player.msg5='circle'

def updateWaiting(event,player):

  pygame.time.wait(500)

  player.waiting=False
  if  player.currentRoom.en4=='1':
    player.msg5='initiating battle...'
    player.traversal=False
    player.battle=True
    enemyList=[Enemy()]
    player.curBattle=BattleEngine(player,enemyList)
    setImage(player)

def updateBattle(event,player):

    player.curBattle.Run(event,screen)

###Draw methods###

def drawTraversal(player,screen):

      setImage(player)

def drawWaiting(player,screen):

      screen.fill(0,(0,0,1290,700),0)



      

setImage(player)

   

while pippy.pygame.next_frame():

  

  for event in pygame.event.get():

    if player.traversal:

      if player.waiting:

        updateWaiting(event,player)

      else:

        #################UPDATE##############################

        updateTraversal(event,player,screen)

    elif player.statMenu:

      ##stat menu processes

      #updateStatMenu

      print(player.stat)

    elif player.battle:

      ##battle processes

      updateBattle(event,player)

      print(player.battle)



    elif player.mainMenu:

      ## main menu processes

      updateMenu(event,player)

      print(player.mainMenu)

    elif player.inTutorial:

      updateTutorial(event,player)



  ###############DRAW#########################

  #draw based on state

  if player.mainMenu:

    player.currentMenu.draw(player,screen,400,500,50)

  else:

    screen.fill(0,bigRect,0)

    # draw the text

    tl1=font.render(player.msg1,True,(255,255,255))

    tl2=font.render(player.msg2,True,(255,255,255))

    tl3=font.render(player.msg3,True,(255,255,255))

    tl4=font.render(player.msg4,True,(255,255,255))

    tl5=font.render(player.msg5,True,(255,255,255))



    player.dgnMap.display(player,screen)

    #screen.blit(text, textRect)

    screen.blit(tl1,line1)

    screen.blit(tl2,line2)

    screen.blit(tl3,line3)

    screen.blit(tl4,line4)

    screen.blit(tl5,line5)

    

    if player.traversal:

      if player.waiting:

        drawWaiting(player,screen)

      else:

        drawTraversal(player,screen)

    elif player.statMenu:

      drawStatMenu(player,screen)

    elif player.battle:

      player.curBattle.draw(player,screen)

    elif player.inTutorial:

      player.tutorial.draw(player.currentRoomGroup,screen)

  if player.traversal:

    player.currentRoomGroup.draw(screen)
    pygame.display.flip()

  # update the display  

  

