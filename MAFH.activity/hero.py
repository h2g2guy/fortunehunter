
#Hero class - represents the player in battle and holds all of their data

##########################################################################
import pippy, pygame, sys, math
from player import *
from item import *
from pygame.locals import *
import os.path

IMG_PATH = os.path.dirname(__file__) + "/images/"
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
	
	self.divArray = [0,0,0,0]	#Used to tally different amount of fractions used.

	self.weapon=Item(player,"","")
	self.armor=Item(player,"","")
	self.accessory=Item(player,"","")
        self.eqItem=[]			#player can equip up to 4 usable items to use in battle
	self.inv_Ar 	= []		#inventory
	self.attacks_Ar = []		#associated array for attack string names and attack power values
        self.currentInput=""
        self.currentProb1=0
        self.currentProb2=0
        self.currentAnswer=0

        basicSword=Item(player,"Sword","Weapon")
        basicArmor=Item(player,"Vest","Armor")
        potion=Item(player,"Potion","Usable")
        grenade=Item(player,"Grenade","Usable")
        basicRing=Item(player,"Ring","Accessory")

        self.equip(basicSword)
        self.equip(basicArmor)
        self.equip(basicRing)
        self.equip(potion)
        self.equip(grenade)
        self.equip(grenade)
        self.equip(potion)
        self.inv_Ar=[basicSword,basicArmor,potion,basicRing]

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
      return self.ATT+self.BAE
    elif name=="critical":
      return self.ATT+self.BAE+self.BAB
    elif name=="Fire":
      return self.ATT+self.BAB
    elif name=="Heal":
      return self.BAB-10
    elif name=="Lightning":
      return self.ATT+self.BAB
    elif name=="Division":
      x = self.divArray.count(1)
      return self.ATT*((x/4) + 1)
    elif name=="Missile":
      return 0

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
    self.BAB = _BAP

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
    if self.HP<0:
      self.HP=0
#****BATTLE ACCESSORS***********************************************#
  #returns player's list of attacks that are currently available for use
  def availableAttacks(self):
    return self.attacks_Ar
      #returns the attack power of a given attack type

#****INVENTORY MUTATORS********************************************#
  #add item to equipment
  def equip(self,item):
    #add  _item to equipment
    if item.type=="Weapon":
      self.weapon=item
      self.BAE=item.power
    elif item.type=="Armor":
      self.armor=item
      self.BDE=item.power
    elif item.type=="Accessory":
      self.accessory=item
      self.BHP=item.power
    else:
      if len(self.eqItem)<4:
        self.eqItem.append(item)
      else:
        self.eqItem.remove(0)
        self.eqip(item)

  #remove item from equipment
  def remEquipment(self,item):
    if item.type=="Weapon":
      self.weapon=0
      self.BAE=0
    elif item.type=="Armor":
      self.armor=0
      self.BDE=0
    elif item.type=="Accessory":
      self.accessory=0
      self.BHP=0
    else:
      if self.eqItem.has(item):
        self.eqItem.remove(item)
    #remove _item from equipment -- leave cell empty

  #add item to inventory
  def addInventory(self,item):
    self.inv_Ar.append(item)
    #add _item to end of inventory

  def remInventory(self,item):
    self.inv_Ar.remove(item)
    #remove _item from inventory
#end class Hero

