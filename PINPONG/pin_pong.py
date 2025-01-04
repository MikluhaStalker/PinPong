#Подключаем модули
from pygame import *
from random import *
import time as tm
#Содаём экран
font.init()
window = display.set_mode((1024, 576))
display.set_caption('PIN_PONG')
background = transform.scale(image.load('fon.png'), (1024, 576))
window.blit(background, (0, 0))
s1 = 'Время до конца: '
win1 = font.SysFont('Arial', 70).render('PLAYER1 WIN!', True, (255, 0, 0))
win2 = font.SysFont('Arial', 70).render('PLAYER2 WIN!', True, (255, 0, 0))
game = True
clock = time.Clock()
FPS = 60
wait = 100
finished = False
#Создание классов
#Общий
class GameSprite(sprite.Sprite):
    def __init__(self, p_image, p_x, p_y, p_speed, p_s_x, p_s_y):
        super().__init__()
        self.image =  transform.scale(image.load(p_image), (p_s_x, p_s_y))
        self.speed = p_speed
        self.rect = self.image.get_rect()
        self.rect.x = p_x
        self.rect.y = p_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
#Игроки
class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_w]:
            self.rect.y -= 16
        if key_pressed[K_s]:
            self.rect.y += 16
    def update2(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_UP]:
            self.rect.y -= 16
        if key_pressed[K_DOWN]:
            self.rect.y += 16
    def restart(self):
        self.rect.x = 0
        self.rect.y = 0
#Мяч
class Ball(GameSprite):
    def __init__(self, p_image, p_x, p_y, p_speed, p_s_x, p_s_y):
        super().__init__(p_image, p_x, p_y, p_speed, p_s_x, p_s_y)
        self.p_sp_x = 10
        self.p_sp_y = 10
    def forward(self):
        self.rect.x += self.p_sp_x 
        self.rect.y += self.p_sp_y
        if sprite.collide_rect(player1, ball):
            self.p_sp_x *= -1
        if sprite.collide_rect(player2, ball):
            self.p_sp_x *= -1
        if self.rect.y >= 576 or self.rect.y <= 0:
            self.p_sp_y *= -1
        if self.rect.x >= 1024 or self.rect.x <= 0:
            self.p_sp_x *= -1
#Надписи
class Text():
    def __init__ (self, x, y, weidth, height, color = (255, 255, 255)):
        self.rect = Rect(x, y, weidth, height)
        self.color = color
    def text(self, text, k = 40):
        font1 = font.SysFont('Arial', k)
        self.question = font1.render(text, True, (255, 255, 255))
    def text_draw(self):
        window.blit(self.question, (self.rect.x, self.rect.y))
clock = time.Clock()
game = True
#Создание экземпляров классов
player1 = Player('player1.png', 100, 100, 20, 20, 100)
player2 = Player('player2.png', 924, 100, 20, 20, 100)
ball = Ball('ball.png', 512, 288, 200, 50, 50)
timer = Text(492, 50, 100, 100, color)
ps1 = Text(312, 288, 200, 100, color)
ps2 = Text(712, 288, 200, 100, color)
win = Text(512, 288, 200, 200, color)
won = Text(512, 288, 200, 200, color)
s1 = 0
s2 = 0
timer.text('0')
ps1.text('0')
ps2.text('0')
#Начало отсчёта времени
start_time = tm.time()
cur_time = start_time
new_time = start_time
#Игровой цикл
while game:
    window.blit(background, (0, 0))
    clock.tick(FPS)
    new_time = tm.time()
    if new_time - cur_time >= 1:
        if new_time - start_time > 300:
            if s1 > s2 or s1 < s2:
                wait = 0
                finished = True
                start_time = tm.time()
            display.update()
        timer.text(str(int(new_time - start_time)))        
        cur_time = new_time
    #Закрытие окна
    for e in event.get():
        if e.type == QUIT:
            game = False
    if not finished:
        #Движение мяча
        if ball.rect.x <= 30:
            s2 = s2 + 1
            ball.rect.x = 512
            ball.rect.y = 288
            if randint(1,2) == 1:
                ball.p_sp_x *= 1
            if randint(1,2) == 2:
                ball.p_sp_x *= -1
            if randint(1,2) == 1:
                ball.p_sp_y *= 1
            if randint(1,2) == 2:
                ball.p_sp_y *= -1 
            ps2.text(str(int(s2)))
        if ball.rect.x >= 950:
            s1 = s1 + 1
            ball.rect.x = 512
            ball.rect.y = 288
            if randint(1,2) == 1:
                ball.p_sp_x *= 1
            if randint(1,2) == 2:
                ball.p_sp_x *= -1
            if randint(1,2) == 1:
                ball.p_sp_y *= 1
            if randint(1,2) == 2:
                ball.p_sp_y *= -1 
            ps1.text(str(int(s1)))
        #ПРименение методов классов
        timer.text_draw()
        ps1.text_draw()
        ps2.text_draw()
        player1.reset()
        player1.update()
        player2.reset()
        player2.update2()
        ball.reset()
        ball.forward()
    else:
        if wait < 100:
            if s1>s2:
                window.blit(win1, (270, 230))
                wait += 1
            if s1<s2:
                window.blit(win2, (270, 230))
                wait += 1
            if wait == 99:
                s1 = 0
                s2 = 0
                wait = 0
                start_time = tm.time()
                ps2.text(str(int(s2)))
                ps1.text(str(int(s1)))
                finished = False
    display.update()