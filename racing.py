# import thư viện
import pygame
import sys
import random
import time
from pygame.locals import *
# thư viện tự viết
import controller.img as IMAGE
import controller.button as button
import constants.obstacle as obstacle
import constants.car as car
import constants.window as window


# icon app
IMAGE.setIconApp()

# window app
WINDOW_WIDTH = window.WINDOW_WIDTH
WINDOW_HEIGHT = window.WINDOW_HEIGHT
X_MARGIN = window.X_MARGIN
LANE_WIDTH = window.LANE_WIDTH
DISTANCE = window.DISTANCE
FPS = window.FPS


# tốc độ car
CAR_WIDTH = car.CAR_WIDTH
CAR_HEIGHT = car.CAR_HEIGHT
CAR_SPEED = car.CAR_SPEED


# init OBSTACLES
# OBSTACLES_IMG = IMAGE.obstacle.redCar()
OBSTACLES_SPEED = obstacle.obstacleSpeed
CHANGE_SPEED = obstacle.changeSpeed
BG_SPEED = obstacle.backgroundSpeed

# list OBSTACLES
carListObstacle = car.carListObstacle

# list car user
carListUser =  car.carListUser
carListUserStart = car.carListUserStart
# img
BG_POSTER = IMAGE.POSTER() # Background trước ghi vào game
BG_IMG = IMAGE.BACKGROUND()
PLAY_BUTTON = IMAGE.PLAY_BUTTON()
HELP_BUTTON = IMAGE.HELP_BUTTON()
RETURN_BUTTON = IMAGE.RETURN_BUTTON()
RELOAD_BUTTON = IMAGE.RELOAD_BUTTON()
INSTRUCTION = IMAGE.INSTRUCTION()
LEFT_BUTTON = IMAGE.LEFT_BUTTON()
RIGHT_BUTTON = IMAGE.RIGHT_BUTTON()
FRAMES = IMAGE.FRAMES()  # khung chứa chọn các xe
CHOOSE_CAR = IMAGE.CHOOSE_CAR()
# init app game
pygame.init()
DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('HORIZON CHASE Tunbo')
fpsClock = pygame.time.Clock()

class Background():
    def __init__(self, img):
        self.x = 0
        self.y = 0
        self.speed = BG_SPEED
        self.img = img
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def draw(self):
        DISPLAY_SURF.blit(self.img, (int(self.x), int(self.y)))
        DISPLAY_SURF.blit(self.img, (int(self.x), int(self.y-self.height)))

    def update(self):
        self.y += self.speed
        if self.y > self.height:
            self.y -= self.height


class Obstacles():
    def __init__(self):
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.distance = DISTANCE
        self.speed = OBSTACLES_SPEED
        self.changeSpeed = CHANGE_SPEED
        self.ls = []
        for i in range(5):
            y = -CAR_HEIGHT-i*self.distance
            lane = random.randint(55, 300)
            carObstacleImg = carListObstacle[random.randint(0, len(carListObstacle) - 1)] # random xe
            self.ls.append([lane, y, carObstacleImg]) # thêm ảnh xe vào mảng

    def draw(self):
        for i in range(5):
            # x = int(X_MARGIN + self.ls[i][0] *
            #         LANE_WIDTH + (LANE_WIDTH-self.width)/2)
            x = int(self.ls[i][0])
            y = int(self.ls[i][1])
            DISPLAY_SURF.blit(self.ls[i][2], (x, y))

    def update(self):
        for i in range(5):
            self.ls[i][1] += self.speed
        self.speed += self.changeSpeed
        if self.ls[0][1] > WINDOW_HEIGHT:
            self.ls.pop(0)
            y = self.ls[3][1] - self.distance
            lane = random.randint(55, 300)
            carObstacleImg = carListObstacle[random.randint(0, len(carListObstacle) - 1)] # random xe
            self.ls.append([lane, y, carObstacleImg]) # thêm ảnh xe vào mảng


class Car():
    def __init__(self, img): # Thêm img vào constructor
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.img = img #
        self.x = (WINDOW_WIDTH-self.width)/2
        self.y = (WINDOW_HEIGHT-self.height)/2
        self.speed = CAR_SPEED
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((255, 255, 255))

    def draw(self):
        DISPLAY_SURF.blit(self.img, (int(self.x), int(self.y)))

    def update(self, moveLeft, moveRight, moveUp, moveDown):
        if moveLeft == True:
            self.x -= self.speed
        if moveRight == True:
            self.x += self.speed
        if moveUp == True:
            self.y -= self.speed
        if moveDown == True:
            self.y += self.speed

        if self.x < X_MARGIN:
            self.x = X_MARGIN
        if self.x + self.width > WINDOW_WIDTH - X_MARGIN:
            self.x = WINDOW_WIDTH - X_MARGIN - self.width
        if self.y < 0:
            self.y = 0
        if self.y + self.height > WINDOW_HEIGHT:
            self.y = WINDOW_HEIGHT - self.height


class Score():
    def __init__(self):
        self.score = 0

    def draw(self):
        font = pygame.font.SysFont('consolas', 30)
        diem = int(self.score)
        # if diem < 40 and diem > 30:
        #     BG_IMG = BG_POSTER
            
        scoreSuface = font.render(
            'Score: '+str(int(self.score)), True, (255, 255, 255))
        DISPLAY_SURF.blit(scoreSuface, (10, 10))

    def update(self):
        self.score += 0.02

    def getScore(self):
        return self.score


def rectCollision(rect1, rect2):
    if rect1[0] <= rect2[0]+rect2[2] and rect2[0] <= rect1[0]+rect1[2] and rect1[1] <= rect2[1]+rect2[3] and rect2[1] <= rect1[1]+rect1[3]:
        return True
    return False


def isGameOver(car, obstacles):
    carRect = [car.x, car.y, car.width - 14, car.height - 10]
    for i in range(5):
        # x = int(X_MARGIN + obstacles.ls[i][0] *
        #         LANE_WIDTH + (LANE_WIDTH-obstacles.width)/2)
        x = int(obstacles.ls[i][0])
        y = int(obstacles.ls[i][1])
        obstaclesRect = [x, y, obstacles.width - 10, obstacles.height - 10]
        if rectCollision(carRect, obstaclesRect) == True:
            return True
    return False

option = 0
def chooseOpitons():
    global option
    print(option)
    option1 = button.Button(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 80, PLAY_BUTTON)
    option2 = button.Button(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, PLAY_BUTTON)
    option1.draw(DISPLAY_SURF)
    option2.draw(DISPLAY_SURF)

    if option1.isClicked:
        option = 1

    if option2.isClicked:
        option = 2


idx = 0
carPlayer1 = carListUserStart[0] # Biến chọn xe người chơi
def chooseCar1(bg):
    global idx
    DISPLAY_SURF.blit(bg, (0, 0))
    playButton = button.Button(WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT - 250, PLAY_BUTTON)
    leftButton = button.Button(0, 280, LEFT_BUTTON)
    rightButton = button.Button(340, 280, RIGHT_BUTTON)
    DISPLAY_SURF.blit(FRAMES, (55, 210))
    DISPLAY_SURF.blit(carListUser[idx], (100, 200))
    playButton.draw(DISPLAY_SURF) 
    leftButton.draw(DISPLAY_SURF)
    rightButton.draw(DISPLAY_SURF)

    if leftButton.isClicked:
        time.sleep(0.3)
        if idx == 0:
            idx = len(carListUser) - 1
        else:
            idx -= 1

    if rightButton.isClicked:
        time.sleep(0.3)
        if idx == len(carListUser) - 1:
            idx = 0
        else:
            idx += 1
    
    if playButton.isClicked:
        return carListUserStart[idx] # chọn xe người chơi

carPlayer2 = carListUserStart[0]
def chooseCar2(bg):
    global carPlayer1
    global carPlayer2
    carPlayer1 = chooseCar1(bg)
    carPlayer2 = chooseCar1(bg)


def gameStart(bg):
    playButton = button.Button(WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT - 380, PLAY_BUTTON)
    helpButton = button.Button(WINDOW_WIDTH - 60, 0, HELP_BUTTON)
    returnButton = button.Button(20, 160, RETURN_BUTTON)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        DISPLAY_SURF.blit(bg, (0, 0))
        playButton.draw(DISPLAY_SURF)
        helpButton.draw(DISPLAY_SURF)

        if helpButton.isClicked:
            DISPLAY_SURF.blit(INSTRUCTION, (-94, 40))
            returnButton.draw(DISPLAY_SURF)
            if returnButton.isClicked:
                gameStart(bg)

        if playButton.isClicked:
            DISPLAY_SURF.blit(bg, (0, 0))
            chooseOpitons()
            if option == 1:
                chooseCar1(bg)
            if option == 2:
                chooseCar2(bg)

        pygame.display.update()
        fpsClock.tick(FPS)


def gamePlay(bg, car, obstacles, score):
    global BG_IMG
    car.__init__(carPlayer1)
    obstacles.__init__()
    bg.__init__(BG_IMG)
    score.__init__()
    moveLeft = False
    moveRight = False
    moveUp = False
    moveDown = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    moveLeft = True
                if event.key == K_RIGHT:
                    moveRight = True
                if event.key == K_UP:
                    moveUp = True
                if event.key == K_DOWN:
                    moveDown = True
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    moveLeft = False
                if event.key == K_RIGHT:
                    moveRight = False
                if event.key == K_UP:
                    moveUp = False
                if event.key == K_DOWN:
                    moveDown = False
        if isGameOver(car, obstacles):
            return
        bg.draw()
        bg.update()
        car.draw()
        car.update(moveLeft, moveRight, moveUp, moveDown)
        obstacles.draw()
        obstacles.update()
        score.draw()
        score.update()

        scoreUser = int(score.getScore())
        scoreNextLevel = random.randint(5, 10)
        if scoreUser == scoreNextLevel:
            # print(diem)
            BG_IMG = BG_POSTER
            bg.__init__(BG_IMG)
        pygame.display.update()
        fpsClock.tick(FPS)


def gameOver(bg, car, obstacles, score):
    reloadButton = button.Button(
        WINDOW_WIDTH/2 - 50, WINDOW_HEIGHT/2 - 30, RELOAD_BUTTON)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        bg.draw()
        car.draw()
        obstacles.draw()
        score.draw()
        reloadButton.draw(DISPLAY_SURF)
        DISPLAY_SURF.blit(IMAGE.GAME_OVER(), (35, 150))

        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == K_SPACE:     
                    return   

        # goi lai gameStart neu muon chon lai xe
        if reloadButton.isClicked:
            # gameStart(BG_POSTER)
            return

        pygame.display.update()
        fpsClock.tick(FPS)


def main():
    gameStart(BG_POSTER)
    bg = Background(BG_IMG)
    car = Car(carPlayer1)
    obstacles = Obstacles()
    score = Score()
    while True:
        gamePlay(bg, car, obstacles, score)
        gameOver(bg, car, obstacles, score)

if __name__ == '__main__':
    main()


# phát triển chức năng đa luồng: 2 player
# Phạm Tùng Dương