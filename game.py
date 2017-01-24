import pygame
import os   # regelt filesystem voor get_image
import random
import sys
import eztext
pygame.init()
display_width = 800
display_height = 600
#kleuren
black = (0, 0, 0)
white = (255, 255, 255)
tint_red = (200, 0, 0)
red = (255, 0, 0)
tint_green = (0, 200, 0)
green = (0, 255, 0)
blue = (0,0,255)
txtbx = eztext.Input(maxlength=20, color=(0, 0, 0), prompt='Name:')
colors = [red,green,blue,black]
#globals
intro, Introduction, gameExit,playing, players, throwdice = True, False, False, False, False, 0
gameDisplay = pygame.display.set_mode((display_width, display_height))  #init resolution
pygame.display.set_caption('Name')  #window naam
clock = pygame.time.Clock()     #nodig voor Refresh Rate
_image_library = {}     #global list

class player(object):
    def __init__(self,name,score,color,gridx,gridy,turn):
        self.name = name
        self.score = score
        self.color = color
        self.gridx = gridx
        self.gridy = gridy
        self.idx = 0
        self.turn = False
    def move(self,x,y):
        self.gridx += x
        self.gridy += y
    def score(self,points):
        self.score += points
    def draw(self):
        pygame.draw.rect(gameDisplay, self.color, (self.gridx, self.gridy, 55, 55))
    def changecolor(self):
        thiselem = colors[self.idx]
        self.idx = (self.idx + 1) % len(colors)
        nextelem = colors[self.idx]
        self.color = thiselem

player1 = player("Henkie", 0, green, 70, 30,0)
player2 = player("Hankie", 0, black, 270, 300,0)
player3 = player("Penkie", 0, blue, 470, 300,0)
player4 = player("Shanghai", 0, red, 670, 300,0)

def get_image(path):    #functie om een foto te tonen
        global _image_library
        image = _image_library.get(path)
        if image == None:
                canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                image = pygame.image.load(canonicalized_path).convert_alpha()
                _image_library[path] = image
        return image

def button(msg,x,y,w,h,ic,ac,action=None):          #functie om een knop te maken (text,x,y,width,height,kleur, hover kleur, actie)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:   #als de muis over de knop hovert, verander de kleur
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if click[0] == 1 and action != None:        #als je er op klikt, doe actie
            action()
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

def dice(x,y):
    part = 0
    if part == 0:
        result = str(random.randint(x,y))
        part = part + 1
    while part <= 180:
        largeText = pygame.font.SysFont("freesansbold.ttf", 115)
        TextSurf, TextRect = text_objects(result, largeText)
        TextRect.center = ((display_width / 2), (display_height / 4))
        gameDisplay.blit(TextSurf, TextRect)
        part = part + 1
        print(part)
        pygame.display.flip()
    else:
        return
def text_objects(text, font):   #functie om tekst te tonen
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def game_intro():   #main menu scherm
    Instruction, Intro, Players = False, True, False
    # ohgodwhy
    x, y, mov_x, mov_y = 0,0,7,7
    while intro:
        x += mov_x
        y += mov_y
        if y > 200 or y < 0:
            mov_y = mov_y * -1
        if x > 750 or x < 0:
            mov_x = mov_x * -1
    #ohgodwhy ends
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        gameDisplay.blit(get_image('logoball.png'), (x, y))
        largeText = pygame.font.SysFont("freesansbold.ttf", 115)
        TextSurf, TextRect = text_objects("Titel", largeText)
        TextRect.center = ((display_width / 2), (display_height / 4))
        gameDisplay.blit(TextSurf, TextRect)
        button("Start", 50, 250, 700, 50, tint_green, green, players)
        button("Instruction", 50, 350, 700, 50, tint_green, green, game_instructions)
        button("Quit", 50, 450, 700, 50, tint_red, red, quit)
        clock.tick(60)      #refresh rate 60 voor smooth ball movement
        pygame.display.flip()


def game_instructions():    #instructie scherm
    Instruction, Intro = True, False
    while Instruction:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        gameDisplay.blit(get_image('koala.jpg'), (150, 50))
        button("Back", 50, 500, 700, 50, tint_green, green, game_intro)
        clock.tick(15)  #refresh rate van 15
        if rolling == True:
            dice(1,6)
            rolling = False
        pygame.display.flip()

def players(): #speler keuze scherm
    intro, Players = False, True
    while Players:
        events = pygame.event.get()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        player1.draw()
        player2.draw()
        player3.draw()
        player4.draw()
        clock.tick(15)  #refresh rate van 15
        txtbx.update(events)
        # blit txtbx on the sceen
        txtbx.draw(gameDisplay)
        button(str(player1.color), 70, 380, 100, 50, tint_green, green, player1.changecolor())
        pygame.display.flip()

def game_main():    #hoofd gamescherm
    Players, Playing = False, True
    while Playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        clock.tick(15)  #refresh rate van 15
        pygame.display.flip()
#roep de schermen op
game_intro()
game_instructions()
game_main()
players()
quit()