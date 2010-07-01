import pygame
import random
from fortuneengine.GameEngineElement import GameEngineElement

from constants import MENU_PATH, PUZZLE_PATH
from gettext import gettext as _

NORMAL_MENU = 1
GRID_MENU = 2

class MagicMenuHolder( GameEngineElement ):
    def __init__(self, callback):
        GameEngineElement.__init__(self, has_draw=True, has_event=False)
        self.menu = None
        self.callback = callback
        self.background = pygame.image.load(MENU_PATH + "battleMenubackground.gif")

    def remove_from_engine(self):
        super( MagicMenuHolder, self ).remove_from_engine()
        self.clear_menu()
        
    def draw(self,screen,time_delta):
        screen.blit(self.background,(0,286,452,414))
        #draw the boxes with the specific magic icons randomly
        
    def menu_called(self, id):
        self.callback(id, self)

    def clear_menu(self):
        if self.menu:
            self.menu.remove_from_engine()
            self.menu = None
            
    def show_menu(self,id):
        if self.is_in_engine():
            self.clear_menu()
        else:
            self.add_to_engine()
        
        
        #example of what will come  
        if id == "fire":
            menu_type = GRID_MENU
            spell_type = 0
            menu_options = [
                        [_('1'), lambda: self.menu_called("fire1"), 140],
                        [_('2'), lambda: self.menu_called("fire2"), 140],
                        [_('3'), lambda: self.menu_called("fire3"), 140],
                        [_('4'), lambda: self.menu_called("fire4"), 140],
                        [_('5'), lambda: self.menu_called("wrongchoice"), 140],
                        [_('6'), lambda: self.menu_called("wrongchoice"), 140],
                        [_('7'), lambda: self.menu_called("wrongchoice"), 140],
                        [_('8'), lambda: self.menu_called("wrongchoice"), 140]
            ]
        elif id == "lightning":
            menu_type = GRID_MENU
            spell_type = 1
            menu_options = [
                        [_('1'), lambda: self.menu_called("lig1"), 140],
                        [_('2'), lambda: self.menu_called("lig2"), 140],
                        [_('3'), lambda: self.menu_called("lig3"), 140],
                        [_('4'), lambda: self.menu_called("lig4"), 140],
                        [_('5'), lambda: self.menu_called("wrongchoice"), 140],
                        [_('6'), lambda: self.menu_called("wrongchoice"), 140],
                        [_('7'), lambda: self.menu_called("wrongchoice"), 140],
                        [_('8'), lambda: self.menu_called("wrongchoice"), 140]
            ]
        elif id == "missile":
            menu_type = GRID_MENU
            spell_type = 2
            menu_options = [
                        [_('1'), lambda: self.menu_called("miss1"), 140],
                        [_('2'), lambda: self.menu_called("miss2"), 140],
                        [_('3'), lambda: self.menu_called("miss3"), 140],
                        [_('4'), lambda: self.menu_called("miss4"), 140],
                        [_('5'), lambda: self.menu_called("wrongchoice"), 140],
                        [_('6'), lambda: self.menu_called("wrongchoice"), 140],
                        [_('7'), lambda: self.menu_called("wrongchoice"), 140],
                        [_('8'), lambda: self.menu_called("wrongchoice"), 140]
            ]
        elif id == "heal":
            menu_type = GRID_MENU
            spell_type = 3
            menu_options = [
                        [_('1'), lambda: self.menu_called("heal1"), 140],
                        [_('2'), lambda: self.menu_called("heal2"), 140],
                        [_('3'), lambda: self.menu_called("heal3"), 140],
                        [_('4'), lambda: self.menu_called("heal4"), 140],
                        [_('5'), lambda: self.menu_called("wrongchoice"), 140],
                        [_('6'), lambda: self.menu_called("wrongchoice"), 140],
                        [_('7'), lambda: self.menu_called("wrongchoice"), 140],
                        [_('8'), lambda: self.menu_called("wrongchoice"), 140]
            ]
        self.menu = MagicMenu(menu_options, 237, 375, menu_type, spell_type)

class MagicMenu(GameEngineElement):
    def __init__(self, magic_menu, x, y, type, spell_type):
        GameEngineElement.__init__(self, has_draw=True, has_event=True)

        self.menu = Menu(magic_menu, spell_type)

        self.menu.set_pos(x, y)
        self.add_to_engine()

    def event_handler(self, event):
        return self.menu.update(event)

    def draw(self,screen,time_delta):
        self.menu.draw( screen )

class Menu(object):
    def __init__(self, options, spelltype):
        """Initialize the EzMenu! options should be a sequence of lists in the
        format of [option_name, option_function]"""

        self.buttons = []
        self.options = options
        self.x = 0
        self.y = 0
        self.cols = 2
        self.option = 0
        self.width = 1
        
        lightning = []
        fire = []
        missile = []
        heal = []
        
        for i in range(1,5):
            fire.append(PUZZLE_PATH + "FireGlyph%dbtn.gif" %i)
            lightning.append(PUZZLE_PATH + "LightningGlyph%dbtn.gif" %i)
            missile.append(PUZZLE_PATH + "MissileGlyph%dbtn.gif" %i)
            heal.append(PUZZLE_PATH + "HealGlyph%dbtn.gif" %i)
        
        if(spelltype == 0):
            #fire attack
            for i in range(4):
                self.buttons.append(pygame.image.load(fire[i]).convert())
            #filler buttons
            for i in range(0,2):
                self.buttons.append(pygame.image.load(lightning[i]).convert())
            random.seed()
            self.buttons.append(pygame.image.load(heal[random.randint(0,3)]).convert())
            self.buttons.append(pygame.image.load(missile[random.randint(0,3)]).convert())
            
            self.mainGlyph = pygame.image.load(PUZZLE_PATH + "FireGlyph.gif").convert()
            
        elif(spelltype == 1):
            #lightning attack
            for i in range(4):
                self.buttons.append(pygame.image.load(lightning[i]).convert())
            #filler buttons
            for i in range(0,2):
                self.buttons.append(pygame.image.load(fire[i]).convert())
            random.seed()
            self.buttons.append(pygame.image.load(heal[random.randint(0,3)]).convert())
            self.buttons.append(pygame.image.load(missile[random.randint(0,3)]).convert())
            
            self.mainGlyph = pygame.image.load(PUZZLE_PATH + "LightningGlyph.gif").convert()
            
        elif(spelltype == 2):
            #missile attack
            for i in range(4):
                self.buttons.append(pygame.image.load(missile[i]).convert())
            #filler buttons
            for i in range(0,2):
                self.buttons.append(pygame.image.load(lightning[i]).convert())
            random.seed()
            self.buttons.append(pygame.image.load(heal[random.randint(0,3)]).convert())
            self.buttons.append(pygame.image.load(fire[random.randint(0,3)]).convert())
            
            self.mainGlyph = pygame.image.load(PUZZLE_PATH + "MissileGlyph.gif").convert()
        elif(spelltype == 3):
            #heal
            for i in range(4):
                self.buttons.append(pygame.image.load(heal[i]).convert())
            #filler buttons
            for i in range(0,2):
                self.buttons.append(pygame.image.load(lightning[i]).convert())
            random.seed()
            self.buttons.append(pygame.image.load(missile[random.randint(0,3)]).convert())
            self.buttons.append(pygame.image.load(fire[random.randint(0,3)]).convert())
            
            self.mainGlyph = pygame.image.load(PUZZLE_PATH + "HealGlyph.gif").convert()
        
        random.seed()
        random.shuffle(self.buttons)
                            
        self.height = (len(self.options)*self.buttons[1].get_height()) / self.cols

    def draw(self, surface):
        """Draw the menu to the surface."""
        i=0 # Row Spacing
        h=0 # Selection Spacing
        j=0 # Col Spacing
        index=0 #current spot in buttons list
        height = self.buttons[0].get_height()
        width = self.buttons[0].get_width()
        
        for o in self.buttons:

            newX = self.x + width * j
            newY = self.y + i * height
            
            if h==self.option:
                pygame.draw.rect(surface, (4, 119, 152), ( newX, newY, height, width))
            surface.blit(self.buttons[index], (newX, newY) )

            j+=1
            h+=1
            index+=1
            if j >= self.cols:
                i+=1
                j=0
                
        surface.blit(self.mainGlyph, (500,350))
    def update(self, event):
        """Update the menu and get input for the menu."""
        return_val = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if self.cols != 1:
                    self.option += self.cols
                else:
                    self.option += 1
                return_val = True
            elif event.key == pygame.K_UP:
                if self.cols != 1:
                    self.option -= self.cols
                else:
                    self.option -= 1
                return_val = True
            elif event.key == pygame.K_RIGHT:
                if self.cols != 1:
                    self.option += 1
                    return_val = True
            elif event.key == pygame.K_LEFT:
                if self.cols != 1:
                    self.option -= 1
                    return_val = True
            elif event.key == pygame.K_RETURN:
                self.options[self.option][1]()
                return_val = True

            self.option = self.option % len(self.options)

        return return_val

    def set_pos(self, x, y):
        """Set the topleft of the menu at x,y"""
        self.x = x
        self.y = y
