from pygame import *
'''Необхідні класи'''
 
# клас-батько для спрайтів
class GameSprite(sprite.Sprite):
    #конструктор класу
    def __init__(self, player_image, player_x, player_y, player_speed, wight, height):
        super().__init__()
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(image.load(player_image), (wight, height)) #разом 55,55 - параметри
        self.speed = player_speed
        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

        # Method for returning of rectangle in which lies our image.
    def getRect(self):
        return self.rect 

# клас-спадкоємець для спрайту-гравця (керується стрілками)    
class Player(GameSprite):
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
 
#ігрова сцена:
background = transform.scale(image.load("pp6.jpg"), (700, 500))  
win_width = 600
win_height = 500
window = display.set_mode((win_width, win_height))
window.blit(background, (0,0))
 
#прапорці, що відповідають за стан гри
game = True
finish = False
clock = time.Clock()
FPS = 60
 
#створення м'яча та ракетки  
racket1 = Player('racket4.png', 30, 200, 4, 50, 150) 
racket2 = Player('racket4.png', 520, 200, 4, 50, 150)
ball = GameSprite('b5.png', 200, 200, 4, 50, 50)

# Ось наша кнопка перезавантаження гри.
butReset = GameSprite('res2.png', 240, 200, 0, 150, 100)

# Це треба для того, щоб спіймати клік мишкою саме по цієї кнопці.
butReset_rect = butReset.getRect()

# Music
mixer.init()
mixer.music.load("sun.ogg")
mixer.music.play()

kick = mixer.Sound('kick.ogg')
winner = mixer.Sound('win.ogg')
out = mixer.Sound('lose.ogg')
 
font.init()
font = font.Font(None, 35)
lose1 = font.render('PLAYER 1 LOSE!', True, (180, 0, 0))
lose2 = font.render('PLAYER 2 LOSE!', True, (180, 0, 0))
win1 = font.render('PLAYER 1 WIN!!!', True, (100, 0, 0))
win2 = font.render('PLAYER 2 WIN!!!', True, (100, 100, 50))
 
speed_x = 3
speed_y = 3

score_1 = 0 
score_2 = 0
 
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        # в цикл додаємо обробку кліка мишею
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1: # це код для обробки лівого кліка миши
                if butReset_rect.collidepoint(e.pos): # це код для обробки лівого кліка саме по нашій картинці
                    
                    # Це персонажі, які мають відтворитися одразу після оновлення гри 
                    finish = False
                    racket1 = Player('racket4.png', 30, 200, 4, 50, 150) 
                    racket2 = Player('racket4.png', 520, 200, 4, 50, 150)
                    ball = GameSprite('b5.png', 200, 200, 4, 50, 50)
                    
                    # Кнопки теж, ми ж будемо все повторювати ще раз.
                    butReset = GameSprite('res2.png', 240, 200, 0, 150, 100)
                    butReset_rect = butReset.getRect()    
  
    if finish != True:
        window.blit(background, (0,0))
        racket1.update_l()
        racket2.update_r()
        ball.rect.x += speed_x
        ball.rect.y += speed_y
    
        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            speed_x *= -1
            speed_y *= 1
            kick.play()
        
        #якщо м'яч досягає меж екрана, змінюємо напрямок його руху
        if ball.rect.y > win_height-50 or ball.rect.y < 0:
            speed_y *= -1
    
        #якщо м'яч відлетів далі ракетки, виводимо умову програшу для першого гравця
        if ball.rect.x < 0 and score_1 < 3:
            finish = True
            score_1 += 1
            window.blit(lose1, (200, 200))
            out.play()

            # Затримуємо надпис
            display.flip()
            time.delay(2000)

            # Відтворюємо кнопку
            butReset.reset()

           
    
        #якщо м'яч полетів далі ракетки, виводимо умову програшу другого гравця
        if ball.rect.x > win_width and score_2 < 3:
            finish = True
            score_2 += 1
            window.blit(lose2, (200, 200))

            out.play()

            # Затримуємо надпис
            display.flip()
            time.delay(2000)

            # Відтворюємо кнопку
            butReset.reset()
            
        if score_1 == 3:
            finish = True
                      
            window.blit(win2, (200, 100))
            window.blit(font.render("Рахунок першого гравця " + str(score_1), True, (50, 50, 50)), (200, 40))

            winner.play()

            # Затримуємо надпис
            display.flip()
            time.delay(2000)

            window.blit(font.render("GAME OVER", True, (250, 50, 50)), (200, 0))

            display.flip()
            time.delay(2000)

        if score_2 == 3:
            finish = True
            
            window.blit(win1, (200, 200))
            window.blit(win2, (200, 100))
            window.blit(font.render("Рахунок ДРУГОГО гравця " + str(score_2), True, (250, 50, 50)), (200, 40))

            winner.play()

            # Затримуємо надпис
            display.flip()
            time.delay(2000)

            window.blit(font.render("GAME OVER", True, (50, 0, 0)), (200, 0)) 

            display.flip()
            time.delay(2000)
            

        racket1.reset()
        racket2.reset()
        ball.reset()
    
    display.update()
    clock.tick(FPS)
