import pygame
import os   # regelt filesystem voor get_image
import random
import time
import eztext
import psycopg2
pygame.init()
pygame.mixer.music.load("Salty_Ditty.wav")
display_width = 800
display_height = 600
#kleuren
black = (0, 0, 0)
white = (255, 255, 255)
tint_red = (200, 0, 0)
red = (255, 0, 0)
tint_green = (0, 200, 0)
green = (0, 255, 0)
tint_blue = (0, 0, 200)
blue = (0,0,255)
lgrey = (240,240,240)
grey = (128,128,128)
#Kleuren voor speler selectie
r = [255,0,0,255,255,0,0]
g = [0,255,0,255,0,255,0]
b = [0,0,255,0,255,255,0]
combined = (r,g,b)
#------------------------------------------------------
#globals
intro, Introduction, gameExit,playing, players, throwdice = True, False, False, False, False, 0
gameDisplay = pygame.display.set_mode((display_width, display_height))  #init resolution
pygame.display.set_caption('Name')  #window naam
clock = pygame.time.Clock()     #nodig voor Refresh Rate
_image_library = {}     #global list
#Database
def db():
    # Connect to an existing database
    conn = psycopg2.connect("dbname=Project2 user=postgres password=wachtwoord")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    cur.execute("SELECT * FROM Players")
    # fetch all of the rows from the query
    data = cur.fetchall ()
# print the rows
    for row in data :
        print("Naam",row[0], "Wins",row[1], "Losses",row[2])
        pygame.display.flip()
        cur.close()

    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()
#------------------------------------------------------
class player(object): #Klasse speler
    def __init__(self,name,score,r,g,b,gridx,gridy,turn):
        self.name = name
        self.score = score
        self.r = r
        self.g = g
        self.b = b
        self.dicenum = "5"
        self.color = (r,g,b)
        self.gridx = gridx
        self.gridy = gridy
        self.idx = 0
        self.turn = False
    def nameinput(self,x,y): #Naam input tekenen
        self.txtbx = eztext.Input(x=x, y=y,maxlength=45, color=(255, 0, 0), prompt='Name: ')
        self.txtbx.value = self.name
    def changepos(self,x,y): #Beweeg de pion
        self.gridx = x
        self.gridy = y
    def move(self,x,y): #Beweeg de pion
        self.gridx += x
        self.gridy += y
    def score(self,points): #Pas de score aan
        self.score += points
    def draw(self): #Teken de pion
        pygame.draw.rect(gameDisplay, (self.color), (self.gridx, self.gridy, 55, 55))
    #Kleur veranderen
    def addr(self):
        self.r = self.r + 1
        if self.r < 0:
            self.r = 255
        if self.r > 255:
            self.r = 0
        self.color = (self.r,self.g,self.b)
    def subr(self):
        self.r = self.r - 1
        if self.r < 0:
            self.r = 255
        if self.r > 255:
            self.r = 0
        self.color = (self.r,self.g,self.b)
    def addb(self):
        self.b = self.b + 1
        if self.b < 0:
            self.b = 255
        if self.b > 255:
            self.b = 0
        self.color = (self.r,self.g,self.b)
    def subb(self):
        self.b = self.b - 1
        if self.b < 0:
            self.b = 255
        if self.b > 255:
            self.b = 0
        self.color = (self.r,self.g,self.b)
    def addg(self):
        self.g = self.g + 1
        if self.g < 0:
            self.g = 255
        if self.g > 255:
            self.g = 0
        self.color = (self.r,self.g,self.b)
    def subg(self):
        self.g = self.g - 1
        if self.g < 0:
            self.g = 255
        if self.g > 255:
            self.g = 0
        self.color = (self.r,self.g,self.b)
    def changecolor(self):
        thiselem = (r[self.idx],g[self.idx],b[self.idx])
        self.idx = (self.idx + 1) % len(r)
        nextelem = r[self.idx]
        self.color = thiselem
#------------------------------------------------------

class dice(object): #Klasse dobbelsteen
    def __init__(self,x,y, num):
        self.x = x
        self.y = y
        self.num = num
        self.duration = 0
    def randomnum(self): #Kies een random nummer
        self.num = random.randint(self.x,self.y)

    def throw(self): #Gooi de dobbelsteen
        while self.duration < random.randint(5,15):
            self.num = random.randint(self.x, self.y)
            gameDisplay.blit(get_image("img/" + str(self.num) + ".png"), (860, 20))
            self.duration = self.duration + 1
            pygame.display.flip()
            print(str(self.duration))
            time.sleep(0.05)
        self.duration = 20
        while self.duration < random.randint(20,28):
            self.num = random.randint(self.x, self.y)
            gameDisplay.blit(get_image("img/" + str(self.num) + ".png"), (860, 20))
            self.duration = self.duration + 1
            pygame.display.flip()
            print(str(self.duration))
            time.sleep(0.2)
        self.duration = 30
        while self.duration < random.randint(30,32):
            self.num = random.randint(self.x, self.y)
            gameDisplay.blit(get_image("img/" + str(self.num) + ".png"), (860, 20))
            self.duration = self.duration + 1
            pygame.display.flip()
            print(str(self.duration))
            time.sleep(0.5)
        self.duration = 40
        while self.duration == 40:
            gameDisplay.blit(get_image("img/" + str(self.num) + ".png"), (860, 20))
            pygame.display.flip()
            time.sleep(2)
            self.duration = 50
        if self.duration == 50:
            if player1.turn == True and player2.turn == False:
                player1.dicenum = str(self.num)
            elif player2.turn == True and player3.turn == False:
                player2.dicenum = str(self.num)
            elif player3.turn == True and player4.turn == False:
                player3.dicenum = str(self.num)
            elif player4.turn == True and player1.turn == False:
                player4.dicenum = str(self.num)
            self.duration = 0
            return

#Spelers defineren
player1 = player("Henkie", 0, 0,255,0, 70, 220,0)
player2 = player("Hankie", 0, 255,255,0, 270, 220,0)
player3 = player("Penkie", 0, 0,0,255, 470, 220,0)
player4 = player("Shanghai", 0, 255,0,0, 670, 220,0)
#Pion defineren
dice1 = dice(1,6,0)




#Tijdelijke code voor aanpassen wie er aan de beurt is
def turnforward():
    if player1.turn == True:
        player1.turn = False
        player2.turn = True
    elif player2.turn == True:
        player2.turn = False
        player3.turn = True
    elif player3.turn == True:
        player3.turn = False
        player4.turn = True
    elif player4.turn == True:
        player4.turn = False
        player1.turn = True

def turnbackward():
    if player1.turn == True:
        player1.turn = False
        player4.turn = True
    elif player2.turn == True:
        player2.turn = False
        player1.turn = True
    elif player3.turn == True:
        player3.turn = False
        player2.turn = True
    elif player4.turn == True:
        player4.turn = False
        player3.turn = True
#------------------------------------------------------
def get_image(path):    #functie om een foto te tonen
        global _image_library
        image = _image_library.get(path)
        if image == None:
                canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                image = pygame.image.load(canonicalized_path).convert_alpha()
                _image_library[path] = image
        return image

def button(msg,x,y,w,h,ic,ac,action=None,action2=None):          #functie om een knop te maken (text,x,y,width,height,kleur, hover kleur, actie)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:   #als de muis over de knop hovert, verander de kleur
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if click[0] == 1 and action != None and action2 == None:        #als je er op klikt, doe actie
            action()
        elif click[0] == 1 and action != None and action2 !=None:        #als je er op klikt, doe actie
            action()
            action2()

    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

def text_objects(text, font):   #functie om tekst te tonen
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def game_intro():   #main menu scherm
    Instruction, Intro, Players, Options = False, True, False, False
    player1.turn = True
    player2.turn, player3.turn, player4.turn = False, False, False
    # ohgodwhy
    x, y, mov_x, mov_y = 0,0,6,6
    while intro:
        x += mov_x
        y += mov_y
        if y > 180 or y < 0:
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
        button("Start", 50, 230, 700, 50, tint_green, green, players)
        button("Instruction", 50, 305, 700, 50, tint_green, green, game_instructions)
        button("Options",50,380,700,50,tint_green, green, game_options)
        button("Highscore", 50, 455, 700, 50, tint_green, green, game_highscore)
        button("Quit", 50, 530, 700, 50, tint_red, red, quit)

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
        gameDisplay.blit(get_image('handleiding.png'), (125, 0))
        button("Back", 50, 0, 100, 50, tint_green, green, game_intro)
        clock.tick(15)  #refresh rate van 15
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
        if player1.turn == True:
            largeText = pygame.font.SysFont("freesansbold.ttf", 115)
            TextSurf, TextRect = text_objects("Player 1", largeText)
            TextRect.center = ((display_width / 2), (display_height / 4))
            player1.nameinput(35,190)
            player1.txtbx.update(events)
            player1.txtbx.draw(gameDisplay)
            player1.name = player1.txtbx.value
            gameDisplay.blit(TextSurf, TextRect)
            button(str(player1.color), 45, 300, 110, 50, tint_green, green, player1.changecolor)
            button("+", 45, 360, 30, 30, tint_red, red, player1.addr)
            button("-", 45, 400, 30, 30, tint_red, red, player1.subr)
            button("+", 85, 360, 30, 30, tint_green, green, player1.addg)
            button("-", 85, 400, 30, 30, tint_green, green, player1.subg)
            button("+", 125, 360, 30, 30, tint_blue, blue, player1.addb)
            button("-", 125, 400, 30, 30, tint_blue, blue, player1.subb)
            button("Next Player", 25, 440, 150, 50, tint_green, green, turnforward)
            button("Back", 50, 500, 700, 50, tint_green, green, game_intro)
        elif player2.turn == True:
            largeText = pygame.font.SysFont("freesansbold.ttf", 115)
            TextSurf, TextRect = text_objects("Player 2", largeText)
            TextRect.center = ((display_width / 2), (display_height / 4))
            player2.nameinput(235,190)
            player2.txtbx.update(events)
            player2.txtbx.draw(gameDisplay)
            player2.name = player2.txtbx.value
            gameDisplay.blit(TextSurf, TextRect)
            smallText = pygame.font.SysFont("freesansbold.ttf", 32)
            textSurf, textRect = text_objects(player1.name, smallText)
            textRect = (35,190)
            gameDisplay.blit(textSurf, textRect)
            button(str(player2.color), 245, 300, 110, 50, tint_green, green, player2.changecolor)
            button("+", 245, 360, 30, 30, tint_red, red, player2.addr)
            button("-", 245, 400, 30, 30, tint_red, red, player2.subr)
            button("+", 285, 360, 30, 30, tint_green, green, player2.addg)
            button("-", 285, 400, 30, 30, tint_green, green, player2.subg)
            button("+", 325, 360, 30, 30, tint_blue, blue, player2.addb)
            button("-", 325, 400, 30, 30, tint_blue, blue, player2.subb)
            button("Next Player", 225, 440, 150, 50, tint_green, green, turnforward)
            button("Back", 50, 500, 700, 50, tint_green, green, turnbackward)
        elif player3.turn == True:
            largeText = pygame.font.SysFont("freesansbold.ttf", 115)
            TextSurf, TextRect = text_objects("Player 3", largeText)
            TextRect.center = ((display_width / 2), (display_height / 4))
            player3.nameinput(435,190)
            player3.txtbx.update(events)
            player3.txtbx.draw(gameDisplay)
            player3.name = player3.txtbx.value
            gameDisplay.blit(TextSurf, TextRect)
            smallText = pygame.font.SysFont("freesansbold.ttf", 32)
            textSurf1, textRect1 = text_objects(player1.name, smallText)
            textRect1 = (35,190)
            textSurf2, textRect2 = text_objects(player2.name, smallText)
            textRect2 = (235,190)
            gameDisplay.blit(textSurf, textRect)
            gameDisplay.blit(textSurf2, textRect2)
            button(str(player3.color), 445, 300, 110, 50, tint_green, green, player3.changecolor)
            button("+", 445, 360, 30, 30, tint_red, red, player3.addr)
            button("-", 445, 400, 30, 30, tint_red, red, player3.subr)
            button("+", 485, 360, 30, 30, tint_green, green, player3.addg)
            button("-", 485, 400, 30, 30, tint_green, green, player3.subg)
            button("+", 525, 360, 30, 30, tint_blue, blue, player3.addb)
            button("-", 525, 400, 30, 30, tint_blue, blue, player3.subb)
            button("Next Player", 425, 440, 150, 50, tint_green, green, turnforward)
            button("Back", 50, 500, 700, 50, tint_green, green, turnbackward)
        elif player4.turn == True:
            largeText = pygame.font.SysFont("freesansbold.ttf", 115)
            TextSurf, TextRect = text_objects("Player 4", largeText)
            TextRect.center = ((display_width / 2), (display_height / 4))
            player4.nameinput(635,190)
            player4.txtbx.update(events)
            player4.txtbx.draw(gameDisplay)
            player4.name = player4.txtbx.value
            gameDisplay.blit(TextSurf, TextRect)
            smallText = pygame.font.SysFont("freesansbold.ttf", 32)
            textSurf1, textRect1 = text_objects(player1.name, smallText)
            textRect1 = (35,190)
            textSurf2, textRect2 = text_objects(player2.name, smallText)
            textRect2 = (235,190)
            textSurf3, textRect3 = text_objects(player3.name, smallText)
            textRect3 = (435,190)
            gameDisplay.blit(textSurf, textRect)
            gameDisplay.blit(textSurf2, textRect2)
            gameDisplay.blit(textSurf3, textRect3)
            button(str(player4.color), 645, 300, 110, 50, tint_green, green, player4.changecolor)
            button("+", 645, 360, 30, 30, tint_red, red, player4.addr)
            button("-", 645, 400, 30, 30, tint_red, red, player4.subr)
            button("+", 685, 360, 30, 30, tint_green, green, player4.addg)
            button("-", 685, 400, 30, 30, tint_green, green, player4.subg)
            button("+", 725, 360, 30, 30, tint_blue, blue, player4.addb)
            button("-", 725, 400, 30, 30, tint_blue, blue, player4.subb)
            button("Play", 625, 440, 150, 50, tint_green, green, game_main)
            button("Back", 50, 500, 700, 50, tint_green, green, turnbackward)
        pygame.display.flip()

def game_highscore():    #Highscore scherm
    # Connect to an existing database
    conn = psycopg2.connect("dbname=Project2 user=postgres password=wachtwoord")

    # Open a cursor to perform database operations
    cur = conn.cursor()
    cur.execute("UPDATE Players SET wins = wins +1 WHERE naam = 'Penkie'")
    cur.execute("SELECT * FROM Players")
    # fetch all of the rows from the query
    data = cur.fetchall ()
# print the rows
    for row in data :
        print("Naam",row[0], "Wins",row[1], "Losses",row[2])
        pygame.display.flip()
        cur.close()

    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()

    Highscore, Intro = True, False
    while Highscore:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        count = 0
        smallText = pygame.font.Font("freesansbold.ttf", 40)
        textSurf, textRect = text_objects("Name", smallText)
        textRect.center = (400, 250)
        gameDisplay.blit(textSurf, textRect)
        smallText = pygame.font.Font("freesansbold.ttf", 40)
        textSurf, textRect = text_objects("Wins", smallText)
        textRect.center = (550, 250)
        gameDisplay.blit(textSurf, textRect)
        smallText = pygame.font.Font("freesansbold.ttf", 40)
        textSurf, textRect = text_objects("Losses", smallText)
        textRect.center = (700, 250)
        gameDisplay.blit(textSurf, textRect)
        for row in data:
            count += 1
            smallText = pygame.font.Font("freesansbold.ttf", 40)
            textSurf, textRect = text_objects(row[0], smallText)
            textRect.center = (400, (250 + (count * 50)))
            gameDisplay.blit(textSurf, textRect)

            smallText = pygame.font.Font("freesansbold.ttf", 40)
            textSurf, textRect = text_objects(str(row[1]), smallText)
            textRect.center = (550, (250 + (count * 50)))
            gameDisplay.blit(textSurf, textRect)

            smallText = pygame.font.Font("freesansbold.ttf", 40)
            textSurf, textRect = text_objects(str(row[2]), smallText)
            textRect.center = (650, (250 + (count * 50)))
            gameDisplay.blit(textSurf, textRect)
        button("Back", 50, 500, 700, 50, tint_green, green, game_intro)
        clock.tick(15)  #refresh rate van 15
        pygame.display.flip()
def game_options():  #opties menu
    Instruction, Intro, Options = False, False, True
    while Options:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        button("Sound off", 50, 130, 350, 50, tint_green, green, sound_off)
        button("Sound on", 400, 130, 350, 50, tint_green, green, sound_on)
        button("Volume down", 50, 230, 350, 50, tint_green, green, volumedown)
        button("Volume up", 400, 230, 350, 50, tint_green, green, volumeup)
        button("Back", 50, 500, 700, 50, tint_red, red, game_intro)
        currentvolume = pygame.mixer.music.get_volume()
        smallText = pygame.font.Font("freesansbold.ttf", 40)
        textSurf, textRect = text_objects(str(round(currentvolume,1)), smallText)
        textRect.center = (400, 350)
        gameDisplay.blit(textSurf, textRect)
        clock.tick(15)  #refresh rate van 15
        pygame.display.flip()

def sound_off():
    pygame.mixer.music.pause()
def sound_on():
    pygame.mixer.music.unpause()

def volumedown():
    volume = pygame.mixer.music.get_volume()
    volume = volume - 0.1
    pygame.mixer.music.set_volume(volume)

def volumeup():
    volume = pygame.mixer.music.get_volume()
    volume = volume + 0.1
    pygame.mixer.music.set_volume(volume)
def drawgamescreen():
    gameDisplay.blit(get_image('euromastbr.png'), (-300, 2))
    gameDisplay.blit(get_image('euromastrb.png'), (-100, 2))
    gameDisplay.blit(get_image('euromastgy.png'), (100, 2))
    gameDisplay.blit(get_image('euromastyg.png'), (300, 2))
    pygame.draw.rect(gameDisplay, lgrey, (800, 0, 600, 700))
    pygame.draw.line(gameDisplay, black, (0, 600), (800, 600), 2)
    pygame.draw.rect(gameDisplay, lgrey, (0, 602, 1024, 200))
    pygame.draw.line(gameDisplay, black, (800, 0), (800, 700), 2)
def drawplayers():
    player1.changepos(890,220)
    player2.changepos(890,330)
    player3.changepos(890,440)
    player4.changepos(890,550)
    player1.draw()
    player2.draw()
    player3.draw()
    player4.draw()
    smallText = pygame.font.SysFont("freesansbold.ttf", 32)
    textSurf1, textRect1 = text_objects(player1.name, smallText)
    textRect1 = (880, 190)
    textSurf2, textRect2 = text_objects(player2.name, smallText)
    textRect2 = (880, 300)
    textSurf3, textRect3 = text_objects(player3.name, smallText)
    textRect3 = (880, 410)
    textSurf4, textRect4 = text_objects(player4.name, smallText)
    textRect4 = (880, 520)
    textSurf5, textRect5 = text_objects(player1.dicenum, smallText)
    textRect5 = (910, 240)
    textSurf6, textRect6 = text_objects(player2.dicenum, smallText)
    textRect6 = (910, 350)
    textSurf7, textRect7 = text_objects(player3.dicenum, smallText)
    textRect7 = (910, 460)
    textSurf8, textRect8 = text_objects(player4.dicenum, smallText)
    textRect8 = (910, 570)
    gameDisplay.blit(textSurf1, textRect1)
    gameDisplay.blit(textSurf2, textRect2)
    gameDisplay.blit(textSurf3, textRect3)
    gameDisplay.blit(textSurf4, textRect4)
    gameDisplay.blit(textSurf5, textRect5)
    gameDisplay.blit(textSurf6, textRect6)
    gameDisplay.blit(textSurf7, textRect7)
    gameDisplay.blit(textSurf8, textRect8)
def game_main():    #hoofd gamescherm
    Players, Playing = False, True
    startinit = 1
    reset = 0
    turn = 0
    helpertext = ""
    display_width = 1024
    display_height = 700
    player1.dicenum = "0"
    player2.dicenum = "0"
    player3.dicenum = "0"
    player4.dicenum = "0"
    gameDisplay = pygame.display.set_mode((display_width, display_height))  # init resolution
    while Playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        clock.tick(15)  #refresh rate van 15
        drawgamescreen()

        smallText = pygame.font.SysFont("freesansbold.ttf", 32)
        textSurf1, textRect1 = text_objects(helpertext, smallText)
        textRect1 = (50, 600)
        gameDisplay.blit(textSurf1, textRect1)
        gameDisplay.blit(get_image('img/empty.png'), (860,20))
        drawplayers()
        if startinit == 1:
            player1.turn = True
            player2.turn = False
            player3.turn = False
            player4.turn = False
            startinit = 0
        if turn == 0:
            if player1.turn == True:
                helpertext = "Speler 1, gooi de dobbelsteen"
                button("Throw", 50, 640, 100, 50, tint_green,green, dice1.throw, turnforward)
            elif player2.turn == True:
                helpertext = "Speler 2, gooi de dobbelsteen"
                button("Throw", 50, 640, 100, 50, tint_green,green, dice1.throw, turnforward)
            elif player3.turn == True:
                helpertext = "Speler 3, gooi de dobbelsteen"
                button("Throw", 50, 640, 100, 50, tint_green,green, dice1.throw, turnforward)
            elif player4.turn == True:
                helpertext = "Speler 4, gooi de dobbelsteen"
                button("Throw", 50, 640, 100, 50, tint_green,green, dice1.throw, turnforward)
        pygame.display.flip()



#roep de schermen op
pygame.mixer.music.play(-1)
game_intro()
game_instructions()
game_main()
game_highscore()
players()

quit()
