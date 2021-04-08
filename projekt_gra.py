#nie posiadam praw autorskich do wszystkich uzytych przeze mnie obrazow i dzwiekow
import pygame
from time import sleep
import random
import pickle
import sys

pygame.init()

#kolory i wielkosci dla gry
green = (102, 255, 51)
grey = (118,119,110)
white = (255, 255, 255)
black = (0,0,0)
bgrey = (148, 166, 154)
red = (256,0,0)
width = 1000
height = 600

#obrazki i poczatkowe rzeczy do zaladowania
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Racing Game")
carimg = pygame.image.load("car1.png")
backgroundleft = pygame.image.load("left.png")
backgroundright = pygame.image.load("right.png")
clock = pygame.time.Clock()
carimg = pygame.image.load("car1.png")
car_width = 23
menu_background = pygame.image.load("b3.jpg")
menu2_background = pygame.image.load("b4.jpg")
acceleration1_sound = pygame.mixer.Sound('f1.wav')
crash_sound = pygame.mixer.Sound("crash.wav")




def button(msg, x, y, wid, heig, text_colour, back_colour, action=None):
    """Creates buttons to navigate through the menu"""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + wid > mouse[0] > x and y + heig > mouse[1] > y:
        pygame.draw.rect(display, back_colour, (x, y, wid, heig))
        if click[0] == 1 and action != None:
            #w zaleznosci od przypisanej akcji, bedzie przenosil do odpowiedniego ekranu
            if action == "play":
                game_loop()
            elif action == "quit":
                pygame.quit()
                quit()
                sys.exit()
            elif action == "instructions":
                instructions()
            elif action == "author":
                author()
            elif action == "results":
                results()
            elif action == "menu":
                menu_loop()
    else:
        pygame.draw.rect(display, text_colour, (x, y, wid, heig))
    small_text = pygame.font.Font("freesansbold.ttf", 20)
    textsurf, textrect = text_object(msg, small_text)
    textrect.center = ((x + (wid / 2)), (y + (heig / 2)))
    display.blit(textsurf, textrect)



def car(x,y):
    """Initializes a player's car"""
    display.blit(carimg, (x,y))



def background():
    """Sets edges of the road"""
    display.blit(backgroundleft, (0, 0))
    display.blit(backgroundright, (700, 0))

def text_object(text, font):
    """Displays text in font that is entered as an argument"""
    textsurface = font.render(text, True, black)
    return textsurface, textsurface.get_rect()


def enemy_car(enemy_start_x, enemy_start_y, enemy):
    """Initializes enemy's car"""
    if enemy == 0: #chce miec tylko jeden samochod w jednym czasie
        enemy_pic = pygame.image.load("car2.png")
    elif enemy == 1:
        enemy_pic = pygame.image.load("car3.png")
    display.blit(enemy_pic, (enemy_start_x, enemy_start_y))

def bonus_sys(bonus_start_x, bonus_start_y, bonus):
    """Generates a bonus"""
    if bonus == 0:
        bonus_pic = pygame.image.load('heart1.jpg')
    if bonus == 1:
        bonus_pic = pygame.image.load('heart2.jpg')
    if bonus == 2:
        bonus_pic = pygame.image.load('star1.jpg')
    if bonus == 3:
        bonus_pic = pygame.image.load('star2.jpg')
    display.blit(bonus_pic, (bonus_start_x, bonus_start_y))


def score_sys(score, lives):
    """Shows score and lives during the game"""
    font = pygame.font.SysFont(None, 40)
    text_score = font.render("Score: " + str(score), True, black)
    text_lives = font.render("Lives: " + str(lives), True, black)
    display.blit(text_score, (800, 30))
    display.blit(text_lives, (800, 60))

def game_over():
    """Screen when user loses"""
    game_over = True
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
        display.blit(menu2_background, (0, 0))
        normaltext = pygame.font.Font("freesansbold.ttf", 50)
        TextSurf, TextRect = text_object("Game over!", normaltext)
        TextRect.center = (480, 200)
        display.blit(TextSurf, TextRect)
        button("Back", 50, 500, 100, 50, white, bgrey, "menu")
        button("Try again", 400, 300, 150, 50, white, bgrey, "play")
        pygame.display.update()
        clock.tick(60)

def result_file(score):
    """Sort scores and save them to the file"""
    #spróbuje go najpierw otworzyc, jeszcze nie wiem czy istnieje
    try:
        file_to_read = open("scores.txt", 'rb')
        scores = pickle.load(file_to_read)
        #file_to_read.close()
    except FileNotFoundError:
        scores = []
        scores.append(score) #dodaje jedyny ktory istnieje
    #jak mam tylko jeden wynik to wystarczy ze tylko z nim porownam
    if len(scores) < 5:
        scores.append(score)
    elif len(scores) == 5:
        for i in range(len(scores)):
            if scores[i] < score:
                scores[4] = score
            else:
                pass

    scores.sort(reverse=True) #od najwiekszego do najmniejszego wyniku
    file = open("scores.txt", 'wb')
    pickle.dump(scores, file)
    file.close()


def results():
    """Screen with best results"""
    results = True
    while results:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
        try :
            file = open("scores.txt", 'rb')
            scores = pickle.load(file)
        except FileNotFoundError:
            scores = []
        big_text = pygame.font.Font("freesansbold.ttf", 70)
        small_text = pygame.font.Font("freesansbold.ttf", 50)
        display.blit(menu2_background, (0, 0))
        if len(scores) == 0:
            textsurf1, textrect1 = text_object("You don't have a best score", big_text)
            textrect1.center = (480, 50)
            display.blit(textsurf1, textrect1)
        else:
            textsurf1, textrect1 = text_object("Your best scores:", big_text) #to do kazdego jesli sa najwyzsze wyniki, a dalej w petli
            textrect1.center = (480, 50)
            display.blit(textsurf1, textrect1)
            if len(scores) >= 1:
                score_1 = str(scores[0])
                textsurf2, textrect2 = text_object("1. " + score_1, small_text)
                textrect2.center = (480, 120)
                display.blit(textsurf2, textrect2)
            if len(scores) >= 2:
                score_2 = str(scores[1])
                textsurf3, textrect3 = text_object("2. " + score_2, small_text)
                textrect3.center = (480, 190)
                display.blit(textsurf3, textrect3)
            if len(scores) >= 3:
                score_3 = str(scores[2])
                textsurf4, textrect4 = text_object("3. " + score_3, small_text)
                textrect4.center = (480, 260)
                display.blit(textsurf4, textrect4)
            if len(scores) >= 4:
                score_4 = str(scores[3])
                textsurf5, textrect5 = text_object("4. " + score_4, small_text)
                textrect5.center = (480, 330)
                display.blit(textsurf5, textrect5)
            if len(scores) >= 5:
                score_5 = str(scores[4])
                textsurf6, textrect6 = text_object("5. " + score_5, small_text)
                textrect6.center = (480, 400)
                display.blit(textsurf6, textrect6)
        button("Back", 50, 500, 100, 50, white, bgrey, "menu")
        pygame.display.update()
        clock.tick(60)


def author():
    """Screen with text about the author"""
    author = True
    while author:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
        display.blit(menu2_background, (0,0))
        normaltext = pygame.font.Font("freesansbold.ttf", 50)
        TextSurf, TextRect = text_object("Hello! I'm Julia", normaltext)
        TextRect.center = (480, 300)
        display.blit(TextSurf, TextRect)
        button("Back", 50, 500, 100, 50, white, bgrey, "menu")
        pygame.display.update()
        clock.tick(60)

def instructions():
    """Screen with instructions about the game"""
    instruction = True
    while instruction:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
        display.blit(menu2_background, (0,0))
        normaltext = pygame.font.Font("freesansbold.ttf", 50)
        smalltext = pygame.font.Font("freesansbold.ttf", 25)
        TextSurf, TextRect = text_object("Description:", normaltext)
        TextRect.center = (480, 50)
        display.blit(TextSurf, TextRect)
        TextSurf1, TextRect1 = text_object("Your goal is to pass as many cars as you only can. ", smalltext)
        TextRect1.center = (480, 100)
        display.blit(TextSurf1, TextRect1)
        TextSurf2, TextRect2 = text_object("The faster you drive, the more points you get.", smalltext)
        TextRect2.center = (480, 130)
        display.blit(TextSurf2, TextRect2)
        TextSurf11, TextRect11 = text_object("You can also gain bonuses, but not all of them are positive", smalltext)
        TextRect11.center = (480, 160)
        display.blit(TextSurf11, TextRect11)
        TextSurf3, TextRect3 = text_object("How to play:", normaltext)
        TextRect3.center = (480, 200)
        display.blit(TextSurf3, TextRect3)
        TextSurf4, TextRect4 = text_object("Use left and right arrow key to move your car", smalltext)
        TextRect4.center = (480, 250)
        display.blit(TextSurf4, TextRect4)
        TextSurf5, TextRect5 = text_object("D - better speed than initial one", smalltext)
        TextRect5.center = (480, 280)
        display.blit(TextSurf5, TextRect5)
        TextSurf6, TextRect6 = text_object("S - more serious speed", smalltext)
        TextRect6.center = (480, 310)
        display.blit(TextSurf6, TextRect6)
        TextSurf7, TextRect7 = text_object("A - most recommended speed", smalltext)
        TextRect7.center = (480, 340)
        display.blit(TextSurf7, TextRect7)
        TextSurf8, TextRect8 = text_object("Warning:", normaltext)
        TextRect8.center = (480, 410)
        display.blit(TextSurf8, TextRect8)
        TextSurf9, TextRect9 = text_object("You can change speed, but once you accelerate", smalltext)
        TextRect9.center = (480, 460)
        display.blit(TextSurf9, TextRect9)
        TextSurf10, TextRect10 = text_object("you cannot drive as slow as on the beginning!", smalltext)
        TextRect10.center = (480, 490)
        display.blit(TextSurf10, TextRect10)
        button("Back", 50, 500, 100, 50, white, bgrey, "menu")
        pygame.display.update()
        clock.tick(60)

def menu_loop():
    """Screen with menu"""
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
        display.blit(menu_background, (0, 0))
        largetext = pygame.font.Font("freesansbold.ttf", 80)
        TextSurf, TextRect = text_object("RACING GAME", largetext)
        TextRect.center = (480, 100)
        display.blit(TextSurf, TextRect)
        button("Start", 400, 200, 150, 50, white, bgrey, "play")
        button("Instructions", 400, 260, 150, 50, white, bgrey, "instructions")
        button("Best results", 400, 320, 150, 50, white, bgrey, "results")
        button("About author", 400, 380, 150, 50, white, bgrey, "author")
        button("Quit", 400, 440, 150, 50, white, bgrey, "quit")

        pygame.display.update()
        clock.tick(50)


def game_loop():
    """Game"""
    x = 400
    y = 540
    x_change = 0
    enemycar_speed = 10
    enemy = random.randint(0, 1)
    enemy_start_x = random.randrange(130, (650 - car_width))
    enemy_start_y = -600
    enemy_width = 23
    enemy_height = 47
    bonus_speed = 15
    bonus = random.randint(0,3)
    bonus_start_x = random.randrange(130, (650 - car_width))
    bonus_start_y = -600
    bonus_width = 38
    bonus_height = 40
    score = 0
    lives = 3


    bumped = False
    while not bumped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:  #przy wcisnietym klawiszu
                if event.key == pygame.K_LEFT:
                    x_change = -10
                if event.key == pygame.K_RIGHT:
                    x_change = 10
                if event.key == pygame.K_a:
                    acceleration1_sound.play()
                    enemycar_speed = 25
                if event.key == pygame.K_s:
                    pygame.mixer.pause()
                    enemycar_speed = 20
                if event.key == pygame.K_d:
                    pygame.mixer.pause()
                    enemycar_speed = 15

            if event.type == pygame.KEYUP:  # przy niewcisnietym
                x_change = 0
        x += x_change
        display.fill(grey)
        background()
        enemy_start_y -= (enemycar_speed / 4)
        enemy_car(enemy_start_x, enemy_start_y, enemy)
        enemy_start_y += enemycar_speed
        bonus_start_y -= (enemycar_speed / 4)
        bonus_sys(bonus_start_x, bonus_start_y, bonus)
        bonus_start_y += bonus_speed
        # bede losowac, zeby mogl tez poruszac sie na x, jednak wieksza szansa, ze bedzie jechal prosto
        enemy_x_change = random.randint(1,5)
        if enemy_x_change == 1:
            enemy_start_x += 4
        car(x, y)
        score_sys(score, lives)
        if x < 130 or x > 700 - car_width: #kiedy wyjedzie poza linie
            crash_sound.play()
            #przenosze go na miejsce poczatkowe, zeby moc odjac zycie
            x = 400
            y = 540
            lives -= 1
        if enemy_start_y > 600:
            enemy_start_y= 0 - enemy_height
            enemy_start_x= random.randrange(130, (650 - car_width))
            enemy = random.randint(0, 1)
            score += int(enemycar_speed/5) #dodaje punkty przy wyminieciu przeciwnika
        if y < enemy_start_y + enemy_height:
            if x > enemy_start_x and x < enemy_start_x + enemy_width or x + car_width > enemy_start_x and x + car_width < enemy_start_x + enemy_width:
                crash_sound.play() #kiedy sie zderzy z przeciwnikiem, sprawdzam czy jest na pozycji startowej
                if x == 400 and y == 540: #jesli tak, to przenosze go gdzies indziej i odejmuje zycie
                    x = 300
                    y = 540
                    lives -= 1
                else:
                    x = 400
                    y = 540
                    lives -= 1
        if y < bonus_start_y + bonus_height:
            if x > bonus_start_x and x < bonus_start_x + bonus_width or x + car_width > bonus_start_x and x + car_width < bonus_start_x + bonus_width:
                if x == 400 and y == 540: #jesli tak, to przenosze go gdzies indziej i odejmuje zycie
                    x = 300
                    y = 540
                    if bonus == 0:
                        lives += 1
                    elif bonus == 1:
                        lives -= 1
                    elif bonus == 2:
                        score += 5
                    elif bonus == 3:
                        score -= 10
                else:
                    x = 400
                    y = 540
                    if bonus == 0:
                        lives += 1
                    elif bonus == 1:
                        lives -= 1
                    elif bonus == 2:
                        score += 5
                    elif bonus == 3:
                        score -= 10

        if bonus_start_y > 600:
            bonus_start_y= 0 - bonus_height
            bonus_start_x= random.randrange(130, (650 - car_width))
            bonus = random.randint(0,3)

        if lives == 0:
            result_file(score)
            game_over()

        pygame.display.update()
        clock.tick(60)

menu_loop()
game_loop()
pygame.quit()
quit()
