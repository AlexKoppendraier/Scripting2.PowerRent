import time
import psycopg2
clock = pygame.time.Clock()
counter, text = 50, '50'.rjust(3)
pygame.time.set_timer(pygame.USEREVENT, 1000)
font = pygame.font.SysFont('Consolas', 30)
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

button("Instruction", 50, 305, 700, 50, tint_green, green, game_instructions)
button("Highscore", 50, 455, 700, 50, tint_green, green, game_highscore)
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
    tut = 0
    while Playing:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    tut = 1
    while tut == 1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    tut = 0
        gameDisplay.fill(white)
        gameDisplay.blit(get_image('img/tutorial.png'), (0,0))
        pygame.display.flip()
game_instructions()
game_highscore()
