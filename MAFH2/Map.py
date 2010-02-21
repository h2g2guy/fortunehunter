import pygame
import math

from constants import (
    NORTH, EAST, WEST, SOUTH,UNLOCKED_DOOR, LOCKED_DOOR, PUZZLE_DOOR,
    LOCKED_PUZZLE_DOOR, ENTRANCE_DOOR, EXIT_DOOR
)
from GameEngine import GameEngineElement

from gettext import gettext as _

class Map(GameEngineElement):
    def __init__(self, dgn):
        GameEngineElement.__init__(self, has_draw=True, has_event=True)

        self.draw_macro_set = False
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
                if dgn.rooms.get((x,y)).get_door('N') != '0':
                    self.fullRooms[(x,y)]=True
                    self.totalSurface.fill((255,255,255),curRect,0)

                elif dgn.rooms.get((x,y)).get_door('S') != '0':
                    self.fullRooms[(x,y)]=True
                    self.totalSurface.fill((255,255,255),curRect,0)

                elif dgn.rooms.get((x,y)).get_door('E') != '0':
                    self.fullRooms[(x,y)]=True
                    self.totalSurface.fill((255,255,255),curRect,0)

                elif dgn.rooms.get((x,y)).get_door('W') != '0':
                    self.fullRooms[(x,y)]=True
                    self.totalSurface.fill((255,255,255),curRect,0)

        self.add_to_engine()

    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            newKey=pygame.key.name(event.key)

            if newKey=='m' or newKey=='[7]':
                self.draw_macro_set = not self.draw_macro_set
                return True

        #Disable other events if macro-map set
        if self.draw_macro_set:
            return True

    def draw(self, screen):
        profile = self.game_engine.get_object('profile')
        x, y = profile.position
        playerFacing = profile.playerFacing

        mapView=pygame.transform.chop(self.totalSurface,(0,0,0,0))
        mapView.fill((255,0,0),( x * 40, y * 40,38,38))

        angle = 0

        if playerFacing==NORTH:
            angle=0
            mapView=pygame.transform.rotate(mapView,angle)
            angle=90
        elif playerFacing==SOUTH:
            angle=180
            mapView=pygame.transform.rotate(mapView,angle)
            angle=270
        elif playerFacing==EAST:
            angle=90
            mapView=pygame.transform.rotate(mapView,angle)
            angle=0
        elif playerFacing==WEST:
            angle=270
            mapView=pygame.transform.rotate(mapView,angle)
            angle=180

        sideDifference=self.sizeX-self.sizeY
        angle=angle*(math.pi/180)
        curSect=pygame.Rect(0,0,200,200)
        curSect.top+=((x*40-81)*math.cos(angle))-((y*40-81)*math.sin(angle))
        curSect.left-=((x*40-81)*math.sin(angle))+((y*40-81)*math.cos(angle))

        if playerFacing==EAST:
            curSect.top+=sideDifference*(40-81)

        elif playerFacing==SOUTH:
            curSect.left+=sideDifference*(40-81)

        map_area = (0,700,200,350)

        mini_map = pygame.Surface( (200,200) )
        mini_map.blit( mapView, curSect )
        screen.fill(0,map_area,0)
        screen.blit(mini_map, map_area)

        if self.draw_macro_set:
            self.draw_macro(self, screen)


    def draw_macro(self,player,screen):
        #DRAW LEGEND
        font=pygame.font.SysFont("cmr10",24,False,False)

        macroMap=pygame.transform.scale(self.totalSurface,(self.sizeX*100,self.sizeY*100))
        screen.fill((0,0,0),(200,0,800,700))
        legend=pygame.Surface((200,300))
        legend.fill((255,0,0),(0,0,40,15))
        legend.blit(font.render(_("LOCKED"),True,(255,0,0)),(45,0,30,5))
        legend.fill((150,255,150),(0,25,40,15))
        legend.blit(font.render(_("OPEN"),True,(150,255,150)),(45,25,30,5))
        legend.fill((255,0,255),(0,50,40,15))
        legend.blit(font.render(_("PUZZLE"),True,(255,0,255)),(45,50,30,5))
        legend.fill((255,255,255),(0,75,40,15))
        legend.blit(font.render(_("EXIT"),True,(255,255,255)),(45,75,30,5))
        legend.fill((50,50,50),(0,100,40,15))
        legend.blit(font.render(_("ENTRANCE"),True,(50,50,50)),(45,100,30,5))
        screen.blit(legend,(800,0,300,300))
        screen.blit(macroMap,(200,0,800,700))

    def update_macro(self):
        profile = self.game_engine.get_object('profile')
        x, y = profile.position
        playerFacing = profile.playerFacing

        self.totalSurface.fill((0,255,0),( x * 40, y * 40,38,38))

        current_room = self.game_engine.get_object('dungeon').rooms[profile.position]

        map_filler = [
                        ('N',(x * 40+5, y * 40,30,5) ),
                        ('S',(x * 40+5, y * 40+35,30,5) ),
                        ('E',(x * 40+35, y * 40+5,5,30) ),
                        ('W',(x * 40, y * 40+5,5,30) )
                     ]

        for dir, filldata in map_filler:

            door_flag = current_room.get_door( dir )

            if door_flag == LOCKED_DOOR or door_flag == LOCKED_PUZZLE_DOOR:
                self.totalSurface.fill( (255,0,0), filldata)

            elif door_flag == UNLOCKED_DOOR:
                self.totalSurface.fill((150,255,150), filldata)

            elif door_flag == PUZZLE_DOOR:
                self.totalSurface.fill((255,0,255), filldata)

            elif door_flag == EXIT_DOOR:
                self.totalSurface.fill((255,255,255), filldata)

            elif door_flag == ENTRANCE_DOOR:
                self.totalSurface.fill((0,0,0), filldata)