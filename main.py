import pygame
from pygame.locals import *
import time
import random

size = 40
bg = (105, 122, 37)
scr_size = (1000,600)

class Apple:
    def __init__(self , parent_screen):
        self.img = pygame.image.load("resource/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = size*4
        self.y = size*4

    def draw(self):
        self.parent_screen.blit(self.img, (self.x,self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,24)*size
        self.y = random.randint(1,14)*size

class Snake:
    def __init__(self,parent_screen,length):
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resource/block.jpg").convert()
        self.direction = 'down'

        self.length = length
        self.x = [size]*length
        self.y = [size]*length

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_left(self):
        if not (self.direction == "right"):
            self.direction = 'left'

    def move_right(self):
        if not (self.direction == "left"):
            self.direction = 'right'

    def move_up(self):
        if not (self.direction == "down"):
            self.direction = 'up'

    def move_down(self):
        if not (self.direction == "up"):
            self.direction = 'down'

    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i -1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'up':
            self.y[0] -=size

        if self.direction == 'down':
            self.y[0] +=size

        if self.direction == 'left':
            self.x[0] -=size

        if self.direction == 'right':
            self.x[0] +=size

        self.draw()

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("SNAKE AND APPLE GAME")

        pygame.mixer.init()
        self.bg_music()

        self.surface = pygame.display.set_mode(scr_size)
        self.snake = Snake(self.surface,1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + size:
            if y1 >= y2 and y1 < y2 + size:
                return True
        return False

    def render_background(self):
        b = pygame.image.load("resource/green.jpg")
        self.surface.blit(b, (0,0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.score()
        pygame.display.flip()

        # snake collision with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            sound = pygame.mixer.Sound("resource/ding.mp3")
            pygame.mixer.Sound.play(sound)
            self.apple.move()
            self.snake.increase_length()

        #snake collision with itself
        for i in range(3,self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                sound = pygame.mixer.Sound("resource/crash.mp3")
                pygame.mixer.Sound.play(sound)
                raise "snake collide"

        # collision with walls
        if not(0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 600):
            sound = pygame.mixer.Sound("resource/crash.mp3")
            pygame.mixer.Sound.play(sound)
            raise "hit the walls error"


    def score(self):
        font = pygame.font.SysFont('cambria',35)
        s = font.render(f"Score : {self.snake.length}", True, (165, 240, 115))
        self.surface.blit(s,(830,10))

    def show_gameover(self):
        self.render_background()
        font1 = pygame.font.SysFont('comicsansms' , 50)
        l1 = font1.render(f"GAME  OVER  ", True, (93, 240, 171))
        self.surface.blit(l1,(340,230))

        font2 = pygame.font.SysFont('arial',40)
        l2 = font2.render(f"Your score is : {self.snake.length} ", True, (93, 240, 171))
        self.surface.blit(l2, (380, 350))

        font3 = pygame.font.SysFont('Times New Roman',30)
        l3  = font3.render(f"Press Enter to play again", True, (168, 227, 217))
        self.surface.blit(l3, (60, 540))
        l4 = font3.render(f"Press Escape to exit ", True, (168, 227, 217))
        self.surface.blit(l4, (720, 540))

        pygame.display.flip()
        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def bg_music(self):
        pygame.mixer.music.load("resource/bg_music_1.mp3")
        pygame.mixer.music.play(-1,0)

    def run(self):
        running = True
        pause  = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_gameover()
                pause = True
                self.reset()

            time.sleep(0.2)


if __name__=="__main__":
    game = Game() 
    game.run()