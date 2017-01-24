import pygame
import os   # regelt filesystem voor get_image
import psycopg2

# Connect to an existing database
conn = psycopg2.connect("dbname=project2 user=postgres password=181aea6e")

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
#cur.execute("CREATE TABLE players (name varchar(10) PRIMARY KEY, wins integer, losses integer);")

# Pass data to fill a query placeholders and let Psycopg perform
# the correct conversion (no more SQL injections!)

#cur.execute("INSERT INTO players (name,wins, losses) VALUES (%s, %s, %s)",
#('test', 10, 2))

# Query the database and obtain data as Python objects

#cur.execute("SELECT * FROM players")
#cur.fetchone()
#(1, 100, "abc'def")

# Make the changes to the database persistent
conn.commit()

# Close communication with the database
cur.close()
conn.close()

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
#globals
intro, Introduction, gameExit = True, False, False
gameDisplay = pygame.display.set_mode((display_width, display_height))  #init resolution
pygame.display.set_caption('Name')  #window naam
clock = pygame.time.Clock()     #nodig voor Refresh Rate
_image_library = {}     #global list

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

def text_objects(text, font):   #functie om tekst te tonen
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def game_intro():   #main menu scherm
    Instruction, Intro = False, True
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
        button("Start", 50, 250, 700, 50, tint_green, green,game_main)
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
        gameDisplay.blit(get_image('euromast1.png'), (0, 0))
        gameDisplay.blit(get_image('euromast2.png'), (0, 0))
        gameDisplay.blit(get_image('euromast3.png'), (0, 0))
        gameDisplay.blit(get_image('euromast4.png'), (0, 0))
        button("Back", 50, 500, 700, 50, tint_green, green, game_intro)
        clock.tick(15)  #refresh rate van 15
        pygame.display.flip()
def game_main():    #hoofd gamescherm
   while gameExit:
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
quit()
