import pygame, sys
from constants import FMC_PATH, MENU_PATH, TOUR_PATH, ENV_PATH, PUZZLE_PATH
import os.path
from random import *
from sugar.activity import activity
import simplejson
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
        self.numPad=False
        self.name=name
        self.inventoryUp=False
        self.player=player
        self.sX=0
        self.xY=0
        i=0

        for name in optionImageFiles:
            sprite=pygame.sprite.Sprite()

            if self.name=="Glyph Menu":
              if player.geomDifficulty==2:
                rotate=90*randint(0,3)
                sprite.image=pygame.transform.rotate(pygame.image.load(name),rotate)
              elif player.geomDifficulty==3:
                rotate=90*randint(0,3)
                flip=randint(0,2)
                sprite.image=pygame.transform.flip(pygame.transform.rotate(pygame.image.load(name),rotate),flip==1,flip==2)
              else:
                sprite.image=pygame.image.load(name)

            else:
              sprite.image=pygame.image.load(name)

            sprite.rectangle=pygame.Rect(0,0,1290,60)
            self.optionsImages.append(sprite)
            i+=1
  
        self.size=i
        self.alphaDrawn=False
        self.titleButton=pygame.image.load(MENU_PATH+"TitleButton.gif")
        self.otherButton=pygame.image.load(MENU_PATH+"Blank.gif")
        self.LArrow=pygame.image.load(MENU_PATH+"LArrow.gif")
        self.XButton=pygame.image.load(TOUR_PATH+"button/buttonX.gif")
        self.RArrow=pygame.image.load(MENU_PATH+"RArrow.gif")
        self.LButton=pygame.image.load(TOUR_PATH+"button/buttonL.gif")
    def mainMenuDraw(self,player,screen,xStart,yStart,height):
        font=pygame.font.SysFont("cmr10",height,False,False)
        self.optionsImages=[]
        for name in self.options:
          self.optionsImages.append(self.titleButton)
        screen.blit(self.background.image,(0,0,1200,900))
        y=xStart
        x=yStart
        i=0
        for name in self.options:
          if i==self.currentOption:
            xMod=20
          else:
            xMod=0
          screen.blit(self.optionsImages[i],(x+xMod,y,200,height))
          if isinstance(self.options[i],Menu):
            screen.blit(font.render(self.options[i].name,True,(50,50,100)),(x+xMod+10,y+10,200,height))
          else:
            screen.blit(font.render(self.options[i],True,(50,50,150)),(x+xMod+10,y+10,200,height))
          y+=height
          i+=1
        pygame.display.flip()

#Title Menu buttons' functions

    #when 'Return to Title' is selected
    def tm_return():
        #return player to the title menu

    #when 'Controls' is selected
    def tm_controls():
        #show the controls for the XO input, let them switch between the two layouts

    #when 'Exit Game' is selected
    def tm_exitGame():
        #exits the game and returns the player to the XO home screen

    #when 'Continue' is selected
    def tm_ap_continue():
        #starts a play of the last 'loaded' game file
		
    #when 'Level Select' is selected
    def tm_ap_levelSelect():
        #allows the player to choose which level to play, from a list of completed levels within a save file

    #when 'Load Game' is selected
    def tm_ap_loadGame():
        #loads a game file into memory, doesn't actually start the game

    #when 'New Game' is selected
    def tm_ap_newGame():
        #creates a new game file to work with, runs new game

    #when 'Play Custom Map' is selected
    def tm_cp_playCustomMap():
        #loads and plays a custom map set created by Fortune Maker

    #when 'New Custom Map' is selected
    def tm_cp_newCustomMap():
        #shows an overview of Fortune Maker and what it can do
        #offers them to quit Fortune Hunter in order to load Fortune Maker

    #when 'Share Map' is selected
    def tm_cp_shareMap():
        #shares (send or receive) custom maps from the directory with friends over local mesh

    #when 'Local Cooperative Play' is selected
    def tm_np_localCoop():
        #starts a game with the option to have a friend join in
        #probably this will just be an option to turn on and off

    #when 'Local Treasure Trekkers Play' is selected
    def tm_np_localTreasure():
        #starts a racing type game and allows players to compete over mesh

    #when 'View Scoreboard' is selected
    def tm_np_scoreboard():
        #shows the classroom scoreboard

    #when 'View Bestiary' is selected
    def tm_np_viewBestiary():
        #shows bestiary of loaded game profile, otherwise shows empty one

    #when 'View Awards' is selected
    def tm_np_viewAwards():
        #shows awards of a loaded game profile, otherwise shows locked ones

    #when 'View Statistics' is selected
    def tm_np_viewStats():
        #shows statistics of a loaded game profile, otherwise shows 0s

    #possibly options menu elements here#

    def pauseMenuDraw(self,player,screen,xStart,yStart,height):
      font=pygame.font.SysFont("cmr10",height,False,False)
      bgSurface=pygame.Surface((1200,900))
      player.currentRoomGroup.draw(bgSurface)
      if self.name=="Inventory":
        self.background.rect=(0,self.sY,1200,900)
      bgSurface.blit(self.background.image,self.background.rect)
      screen.blit(bgSurface,(0,0,1200,900))
      ###BUTTON STUFF??###
      if self.name=="Stats":
          hp=font.render("HP: "+repr(player.battlePlayer.HP),True,(0,0,0))
          hpRect=pygame.Rect(635,425,200,42)
          screen.blit(hp,hpRect)

          player.akhalSprite.rect=(600,350,50,50)
          akhalGroup=pygame.sprite.Group(player.akhalSprite)
          akhalGroup.draw(screen)
          akhal=font.render(repr(player.battlePlayer.akhal),True,(0,0,0))
          akhalRect=pygame.Rect(650,375,200,42)
          screen.blit(akhal,akhalRect)
          att=font.render("ATK: "+repr(player.battlePlayer.attackPower("basic")),True,(0,0,0))
          attRect=pygame.Rect(635,445,200,42)
          screen.blit(att,attRect)
          defense=font.render("DEF: "+repr(player.battlePlayer.defensePower()),True,(0,0,0))
          defenseRect=pygame.Rect(635,465,200,42)
          screen.blit(defense,defenseRect)
          #define rectangles
          weaponRect=pygame.Rect(635,500,200,42)
          self.optionsImages[0].rect=weaponRect
          armorRect=pygame.Rect(635,535,200,42)
          self.optionsImages[1].rect=armorRect
          accessoryRect=pygame.Rect(635,570,200,42)
          self.optionsImages[2].rect=accessoryRect
          itemRect=pygame.Rect(508,435,200,42)
          self.optionsImages[self.currentOption].rect.top-=5
          self.optionsImages[self.currentOption].rect.width=115
          self.optionsImages[self.currentOption].rect.height=33
          screen.fill((125,125,255),self.optionsImages[self.currentOption].rect)
          #draw dynamic text
          if player.battlePlayer.weapon==None:
            wp="Weapon"
          else:
            wp=player.battlePlayer.weapon.name
          if player.battlePlayer.armor==None:
            arm="Armor"
          else:
            arm=player.battlePlayer.armor.name
          if player.battlePlayer.accessory==None:
            acc="Accessory"
          else:
            acc=player.battlePlayer.accessory.name

          weapon=font.render(wp,True,(0,0,0))
          screen.blit(weapon,weaponRect)
          armor=font.render(arm,True,(0,0,0))
          screen.blit(armor,armorRect)
          accessory=font.render(acc,True,(0,0,0))
          screen.blit(accessory,accessoryRect)
          screen.fill((255,150,150),(502,417,123,98))
          screen.fill((150,255,150),(502,511,123,99))
          screen.blit(self.LArrow,(504,450,20,20))
          screen.blit(pygame.transform.scale(self.XButton,(50,50)),(550,450,20,20))
          screen.blit(self.RArrow,(575,550,20,20))
          screen.blit(pygame.transform.scale(self.LButton,(50,50)),(520,540,20,20))

          if player.invTutorial==False:
            k=0
            screen.fill((255,255,255),(0,0,400,400))
            lines=["This is the statistics screen.","Here, you can view information","about your character,","and any items, you have equipped.","As  you can see, there are slots for","weapon,armor,and accessory","as well as 4 slots for items.","To equip an item, select which slot","you want to equip to","and press enter or "] #draw check
            screen.blit(pygame.image.load(TOUR_PATH+"button/"+"buttonV.gif"),(225,375,40,40))
            for message in lines:
              screen.blit(font.render(message,True,(0,200,0)),(20,20+k,200,300))
              k+=40

      elif self.name=="Inventory":
          y=140
          sel=0
          screen.blit(font.render("Inventory:",True,(0,0,0)),(self.sX+80,self.sY+100,200,40))
          for item in player.battlePlayer.inv_Ar:
            if sel==self.currentOption:
              screen.fill((50,50,250),pygame.Rect(self.sX+40,self.sY+y,200,40))
            screen.blit(font.render(item.name,True,(0,0,0)),pygame.Rect(self.sX+40,self.sY+y,200,40))
            y+=40
            sel+=1
            if y==400:
              y=0
              x+=200
          screen.fill((255,150,150),(500,555,125,50))
          screen.fill((150,255,150),(625,555,127,50))
          screen.blit(self.LArrow,(504,560,20,20))
          screen.blit(pygame.transform.scale(self.XButton,(40,40)),(550,560,20,20))
          screen.blit(self.RArrow,(710,560,20,20))
          screen.blit(pygame.transform.scale(self.LButton,(40,40)),(675,560,20,20))
          if player.invTutorial==False:
            screen.fill((250,250,250),(900,300,800,400))
            k=0
            lines=["This list shows the items","you are carrying.  To equip","an item in the current slot,","select one with the arrow","keys, and press enter or","      If the item cannot","be equipped in that","slot, you will be taken back","to the stats screen"]
            for message in lines:
              screen.blit(font.render(message,True,(0,200,0)),(900,300+k,200,300))
              k+=40
            screen.blit(pygame.image.load(TOUR_PATH+"button/"+"buttonV.gif"),(1165,460,40,40))

      elif self.name=="Pause Menu":
          font=pygame.font.SysFont("cmr10",40,False,False)
          screen.blit(font.render("Options",True,(0,0,0)),(525,200,0,0))
          font=pygame.font.SysFont("cmr10",24,False,False)
         
          i=0
          x=550
          y=250
          for name in self.options:
            if self.currentOption==i:
              xMod=30
            else:
              xMod=0
            screen.blit(self.otherButton,(x+xMod,y,0,0))
            screen.blit(font.render(self.options[i],True,(20,20,100)),(x+10+xMod,y+10,0,0))
            i+=1
            y+=50
          screen.fill((255,150,150),(500,555,125,50))
          screen.fill((150,255,150),(625,555,127,50))
          screen.blit(self.LArrow,(504,560,20,20))
          screen.blit(pygame.transform.scale(self.XButton,(40,40)),(550,560,20,20))
          screen.blit(self.RArrow,(710,560,20,20))
          screen.blit(pygame.transform.scale(self.LButton,(40,40)),(675,560,20,20))

      elif self.name=="Math Stats":
          font=pygame.font.SysFont("cmr10",40,False,False)
          screen.blit(font.render("Math Stats",True,(0,0,0)),(525,120,0,0))
          font=pygame.font.SysFont("cmr10",24,False,False)
          screen.blit(font.render("Multiplication problems:",True,(0,0,50)),(510,160,0,0))
          screen.blit(font.render("Easy: "+repr(player.multiplicationStats[0][0])+"/"+repr(player.multiplicationStats[0][1]),True,(0,50,0)),(550,200,0,0))
          screen.blit(font.render("Medium: "+repr(player.multiplicationStats[1][0])+"/"+repr(player.multiplicationStats[1][1]),True,(0,50,0)),(550,225,0,0))
          screen.blit(font.render("Hard: "+repr(player.multiplicationStats[2][0])+"/"+repr(player.multiplicationStats[2][1]),True,(0,50,0)),(550,250,0,0))
          screen.blit(font.render("Fraction problems:",True,(0,0,50)),(510,300,0,0))
          screen.blit(font.render("Easy: "+repr(player.divisionStats[0][0])+"/"+repr(player.divisionStats[0][1]),True,(0,50,0)),(550,340,0,0))
          screen.blit(font.render("Medium: "+repr(player.divisionStats[1][0])+"/"+repr(player.divisionStats[1][1]),True,(0,50,0)),(550,365,0,0))
          screen.blit(font.render("Hard: "+repr(player.divisionStats[2][0])+"/"+repr(player.divisionStats[2][1]),True,(0,50,0)),(550,390,0,0))
          screen.blit(font.render("Geometry problems:",True,(0,0,50)),(510,420,0,0))
          screen.blit(font.render("Easy: "+repr(player.geometryStats[0][0])+"/"+repr(player.geometryStats[0][1]),True,(0,50,0)),(550,455,0,0))
          screen.blit(font.render("Medium: "+repr(player.geometryStats[1][0])+"/"+repr(player.geometryStats[1][1]),True,(0,50,0)),(550,480,0,0))
          screen.blit(font.render("Hard: "+repr(player.geometryStats[2][0])+"/"+repr(player.geometryStats[2][1]),True,(0,50,0)),(550,505,0,0))
          screen.blit(font.render("Puzzles solved:",True,(0,0,50)),(510,535,0,0))
          screen.blit(font.render(repr(player.puzzlesSolved),True,(0,50,0)),(670,535,0,0))
          screen.fill((255,150,150),(500,555,125,50))
          screen.fill((150,255,150),(625,555,127,50))
          screen.blit(self.LArrow,(504,560,20,20))
          screen.blit(pygame.transform.scale(self.XButton,(40,40)),(550,560,20,20))
          screen.blit(self.RArrow,(710,560,20,20))
          screen.blit(pygame.transform.scale(self.LButton,(40,40)),(675,560,20,20))
      elif self.name=="Victory":
          screen.blit(font.render("You Win!",True,(0,15,0)),(530,230,0,0))
          player.akhalSprite.rect=(530,300,50,50)
          akhalGroup=pygame.sprite.Group(player.akhalSprite)
          akhalGroup.draw(screen)
          screen.blit(font.render(repr(self.player.curBattle.checkValue()),True,(0,15,0)),(580,325,0,0))
          k=0
          for message in player.curBattle.battleItems:
            screen.blit(font.render(message,True,(0,15,0)),(520,350+k,200,300))
            k+=40
      elif self.name=="Defeat":
          if not self.alphaDrawn:
            alphaLayer=pygame.image.load(ENV_PATH+"Black.gif")
            alphaLayer.set_alpha(70)
            screen.blit(alphaLayer,(0,0,1200,900))
          self.alphaDrawn=True
          font=pygame.font.SysFont("cmr10",40,False,False)
          screen.blit(font.render("You have been defeated",True,(150,0,0)),(450,400,0,0))
          font=pygame.font.SysFont("cmr10",24,False,False)
          screen.blit(font.render("Continue",True,(150,0,0)),(520,515,0,0))
          screen.blit(font.render("Exit",True,(150,0,0)),(760,515,0,0))
          #draw player stats
          screen.blit(font.render("Multiplication problems right/wrong:",True,(150,0,0)),(20,20,0,0))
          screen.blit(font.render("Easy: "+repr(player.multiplicationStats[0][0])+"/"+repr(player.multiplicationStats[0][1]),True,(150,0,0)),(100,50,0,0))
          screen.blit(font.render("Medium: "+repr(player.multiplicationStats[1][0])+"/"+repr(player.multiplicationStats[1][1]),True,(150,0,0)),(100,80,0,0))
          screen.blit(font.render("Hard: "+repr(player.multiplicationStats[2][0])+"/"+repr(player.multiplicationStats[2][1]),True,(150,0,0)),(100,110,0,0))
          screen.blit(font.render("Fraction problems right/wrong:",True,(150,0,0)),(450,20,0,0))
          screen.blit(font.render("Easy: "+repr(player.divisionStats[0][0])+"/"+repr(player.divisionStats[0][1]),True,(150,0,0)),(530,50,0,0))
          screen.blit(font.render("Medium: "+repr(player.divisionStats[1][0])+"/"+repr(player.divisionStats[1][1]),True,(150,0,0)),(530,80,0,0))
          screen.blit(font.render("Hard: "+repr(player.divisionStats[2][0])+"/"+repr(player.divisionStats[2][1]),True,(150,0,0)),(530,110,0,0))
          screen.blit(font.render("Geometry problems right/wrong:",True,(150,0,0)),(830,20,0,0))
          screen.blit(font.render("Easy: "+repr(player.geometryStats[0][0])+"/"+repr(player.geometryStats[0][1]),True,(150,0,0)),(910,50,0,0))
          screen.blit(font.render("Medium: "+repr(player.geometryStats[1][0])+"/"+repr(player.geometryStats[1][1]),True,(150,0,0)),(910,80,0,0))
          screen.blit(font.render("Hard: "+repr(player.geometryStats[2][0])+"/"+repr(player.geometryStats[2][1]),True,(150,0,0)),(910,110,0,0))
          screen.blit(font.render("Puzzles solved:"+repr(player.puzzlesSolved),True,(150,0,0)),(400,160,0,0))

      pygame.display.flip()


    def battleDraw(self,player,screen,xStart,yStart,height):
        font=pygame.font.SysFont("cmr10",24,False,False)
        screen.blit(self.background.image,self.background.rect)
        if self.numPad:
          if self.name=="GeomTut3" or self.name=="Glyph Menu":
            x=2
          else:
            x=3
          i=0
          sel=0
          for image in self.optionsImages:
            if i==x:
              i=0
              yStart+=height
            if self.options[sel]=="Enter Answer" or self.options[sel]=="Enter":
              yStart+=height
              i=0
            image.rect=pygame.Rect(xStart+(i*height),yStart,height,height)
            if sel==self.currentOption:
              fillRect=image.rect
              fillRect.top-=5
              fillRect.left-=5
              fillRect.width+=10
              fillRect.height+=10
              screen.fill((50,50,255),fillRect,0)
            screen.blit(image.image,image.rect)
            i+=1
            sel+=1


        else:
          y=yStart
          x=xStart
          i=0
          for option in self.options:
            if i==self.currentOption:
              xMod=30
            else:
              xMod=0
            screen.blit(self.otherButton,(x+xMod,y,200,height))
            if isinstance(option,Menu):
              screen.blit(font.render(option.name,True,(50,50,100)),(x+xMod+10,y+10,200,height))
            else:
              screen.blit(font.render(option,True,(50,50,100)),(x+xMod+10,y+10,200,height))
            y+=height
            i+=1
    

      
      ###########KEEPING AS A REFERENCE FOR WHEN I MAKE A BETTER TUTORIAL SYSTEM##############3
      #  if self.name=="AtkTut":
      #    screen.fill((255,255,255),(600,400,400,300))
      #    lines=["To perform a basic attack","select the attack button"]
      #    y=0
      #    for message in lines:
      #      screen.blit(font.render(message,True,(0,200,0)),(600,400+y,400,300))
      #      y+=40
      #######################################################################################
    def select(self,direction):
        if direction=="up":
            if self.currentOption>0:
                self.currentOption-=1

            else:
                self.currentOption=0
        else:
            if self.currentOption<self.size-1:
                self.currentOption+=1

            else:
                self.currentOption=self.size-1

    def progress(self,player,screen):
        if type(self.options[self.currentOption])==type(self):
            player.currentMenu=self.options[self.currentOption]
           # player.previousMenu=self
           # player.currentMenu.sX=player.previousMenu.startX+200
           # player.currentMenu.sY=player.previousMenu.startY+player.previousMenu.currentOption*player.previousMenu.height
        else:
            self.updateByName(self.options[self.currentOption],player,screen)

    def regress(self,player):
        if self.name=="Stats":
          player.mainMenu=False
          player.traversal=True
        else:
          temp=player.currentMenu
          player.currentMenu=player.previousMenu
          player.previousMenu=temp

    def updateByName(self,name,player,screen):
        if name=="New Game":
            player.dgnIndex=-1
            player.playerFacing=1
            player.traversal=False
            player.mainMenu=False
            player.startComic(FMC_PATH+"FMC1/",None)
            player.inComic=True
            pygame.display.flip()

        elif name=="Exit Game":
            sys.exit()
			
        elif name=="Save":
          dataList=player.toString()
          FILE=open(os.path.join(activity.get_activity_root(),"data/"+player.name+".txt"),"w")
          FILE.write(simplejson.dumps(dataList))
          FILE.close()
          #do save stuff
        elif name=="Main Menu":
          player.traversal=False
          player.currentMenu=player.MainMenu
          player.mainMenu=True
        elif name=="Return to Game":
          player.traversal=True
          player.mainMenu=False
		  
        elif name=="Controls":
            player.inTutorial=True
            player.inComic=True
            player.mainMenu=False
            player.startComic(TOUR_PATH+"setup/",None)
			
        elif name=="OFF":  #was disable
          if player.previousMenu.currentOption==0:
            player.critDifficulty=0
          elif player.previousMenu.currentOption==1:
            player.divDifficulty=0
          elif player.previousMenu.currentOption==2:
            player.geomDifficulty=0
          elif player.previousMenu.currentOption==3:
            player.shopDifficulty=1
          player.currentMenu=player.previousMenu
        elif name=="ON":   #was easy
          if player.previousMenu.currentOption==0:
            player.critDifficulty=1
          elif player.previousMenu.currentOption==1:
            player.divDifficulty=1
          elif player.previousMenu.currentOption==2:
            player.geomDifficulty=1
          elif player.previousMenu.currentOption==3:
            player.shopDifficulty=1
          player.currentMenu=player.previousMenu
#remove following code til the next #------------------------
        elif name=="Medium":
          if player.previousMenu.currentOption==0:
            player.critDifficulty=2
          elif player.previousMenu.currentOption==1:
            player.divDifficulty=2
          elif player.previousMenu.currentOption==2:
            player.geomDifficulty=2
          elif player.previousMenu.currentOption==3:
            player.shopDifficulty=2
          player.currentMenu=player.previousMenu
        elif name=="Hard":
          if player.previousMenu.currentOption==0:
            player.critDifficulty=3
          elif player.previousMenu.currentOption==1:
            player.divDifficulty=3
          elif player.previousMenu.currentOption==2:
            player.geomDifficulty=3
          elif player.previousMenu.currentOption==3:
            player.shopDifficulty=2
          player.currentMenu=player.previousMenu
#-------------------------------------------------------------------------------

#Load game - we want to load the profile, but not start a level. Continue will actually start the level
        elif name=="Load Game":
           FILE=open(os.path.join(activity.get_activity_root(),"data/"+player.name+".txt"),"r")
           data=simplejson.loads(FILE.read())
           print(data)
           player.fromData(data)
           
           player.dgnMap.updateMacro(player)
           player.traversal=True
           player.mainMenu=False
           setImage(player)
           player.currentRoomGroup.draw(screen)
           pygame.display.flip()

        elif name=="Return":
          player.currentMenu.currentOption=0
          player.currentMenu=player.MainMenu
		  
        elif name=="Attack":
          if player.critDifficulty>0:
            seed()
            crit=randint(0,2)
            if crit==1:
              player.curBattle.critical(player)
            else:
              player.curBattle.attack(player.battlePlayer,"basic")
          else:
            player.curBattle.attack(player.battlePlayer,"basic")
        elif name=="0" or name=="1"or name=="2" or name=="3" or name=="4" or name=="5" or name=="6" or name=="7"or name=="8"or name=="9":
          if len(player.battlePlayer.currentInput)<7:
            player.battlePlayer.currentInput+=name
        elif name=="Clear":
          player.battlePlayer.currentInput=""
        elif name=="Enter Answer":
          if not player.battlePlayer.currentInput =="":
            if player.battlePlayer.currentAnswer==int(player.battlePlayer.currentInput):
              player.curBattle.attack(player.battlePlayer,"critical")
            else:
              tup=self.player.multiplicationStats[self.player.critDifficulty-1]
              tup=(tup[0],tup[1]+1)
              self.player.multiplicationStats[self.player.critDifficulty-1]=tup
              player.curBattle.attack(player.battlePlayer,"basic")
          else:
            tup=self.player.multiplicationStats[self.player.critDifficulty-1]
            tup=(tup[0],tup[1]+1)
            self.player.multiplicationStats[self.player.critDifficulty-1]=tup
            player.curBattle.attack(player.battlePlayer,"basic")
        elif name=="Division": 
          player.curBattle.divisionAttack()
        elif name[1:2]=="/":
	  player.battlePlayer.fractionSum += float(name[0])/float(name[2])
	  player.curBattle.checkFraction()
        elif name=="Geometry":
          player.curBattle.magic(player)
        elif name=="Fire" or name=="Lightning" or name=="Heal" or name=="Missile":
          player.battlePlayer.currentProb1=""
          player.battlePlayer.currentProb2=""
          player.battlePlayer.currentInput=""
          player.curBattle.startGlyph(name)
	elif name=="Fire1" or name=="Fire2" or name=="Fire3" or name=="Fire4" or name=="Heal1" or name=="Heal2" or name=="Heal3" or name=="Heal4" or name=="Lightning1" or name=="Lightning2" or name=="Lightning3" or name=="Lightning4" or name=="Missile1" or name=="Missile2" or name=="Missile3" or name=="Missile4":
	  player.curBattle.checkGlyph(name)
        elif name=="Scan":
          player.curBattle.scanEnemy()
        elif name=="Item1" or name=="Item2" or name=="Item3" or name=="Item4":
          index=int(repr(name)[5])-1
          if index<len(player.battlePlayer.eqItem):
            player.curBattle.useItem(player.battlePlayer.eqItem[index])
          else:
            player.currentMenu=player.curBattle.battleMenu
	  #if we decide to add puzzle/minigame items, here's where they'd go
        elif name=="Weapon" or name=="Armor" or name=="Accessory":
          self.createInventory(player)
  
        elif name[0:9]=="Equipment":
          player.battlePlayer.equip(player.battlePlayer.inv_Ar[int(name[9:len(name)])])
          player.invTutorial=True
          player.currentMenu=player.statsMenu
          player.currentRoomGroup.draw(screen)
        elif name=="Wrong":
          print("Wrong choice")
        elif name=="Enter":
          player.currentMenu=player.divMenu
        elif name=="Not":
          player.migrateMessages("Incorrect glyph.  Spell fizzles")
          tup=self.player.divisionStats[self.player.divDifficulty-1]
          tup=(tup[0],tup[1]+1)
          self.player.divisionStats[self.player.divDifficulty-1]=tup
          player.curBattle.glyphGroup.empty()
          player.curBattle.glyphOverlayGroup.empty()
          player.curBattle.playerTurn=False
          player.currentMenu=player.curBattle.battleMenu
        elif name=="Continue":
            player.mainMenu=False
            player.traversal=True
            player.battlePlayer.akhal+=player.curBattle.enemyValue
        elif name=="LoseContinue":
           # player.currentX=player.dgn
           # player.currentY=player.dgn
            player.playerFacing=1
            player.nextDungeon(True)
            player.dgnMap.updateMacro(player)
            player.traversal=True
            player.mainMenu=False
            player.battlePlayer.MHP-=2
            player.battlePlayer.HP=player.battlePlayer.MHP
            player.currentRoomGroup.draw(screen)
            pygame.display.flip()
        elif name=="LoseExit":
	    for i in range(6):
              player.migrateMessages("")
            player.__init__(0,0)
            player.traversal=False
            player.mainMenu=True
            player.currentMenu=player.MainMenu
            player.currentMenu.draw(player,screen,0,0,45)
            pygame.display.flip()
	else:
	    sys.exit()

    def createInventory(self,player):
      invOptions=[]
      invImages=[]
      ##Create a 10X2 menu of all items in player's inventory
      ##TODO: make scrollable
      x=0
      y=0
      i=0
      for item in player.battlePlayer.inv_Ar:
        invOptions.append("Equipment"+repr(i))
        i+=1
        invImages.append(MENU_PATH+"Blank.gif")
      player.inventoryMenu=Menu(invOptions,player,MENU_PATH+"VictoryScreen.gif",invImages,"Inventory")
     
      player.inventoryMenu.sX=485
      player.inventoryMenu.sY=11
     # self.inventoryMenu.bgSurface=self.bgSurface
      player.currentMenu=player.inventoryMenu

