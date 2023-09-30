import pygame
import random

#declaração de constantes
PADDLE_SIZE = 200
PADDLE_THICKNESS = 10
LEFT_PADDLE_OFFSET = 20
RIGHT_PADDLE_OFFSET = 770
PADDLE_SPEED = 10
BALL_SIZE = 20
BALL_SPEED = 10
SCREEN_SIZE = (800, 600)

pygame.font.init()
POINTS_FONT = pygame.font.SysFont('Courier', 50)

#classe da raquete utilizada tanto para a raquete da esquerda como para a da direita
class Paddle:
    #construtor da classe
    def __init__(self, size, thickness, offset, speed):
        self.size = size
        self.thickness = thickness
        self.offset = offset
        self.surface = pygame.Surface((thickness, size))
        self.surface.fill((0, 255, 0))
        self.rect = self.surface.get_rect()
        self.rect.x = offset
        self.rect.y = SCREEN_SIZE[1] / 2 - size / 2
        self.speed = speed

    #função para mover a raquete
    def move(self, x, y):
        self.rect.x += x * self.speed
        self.rect.y += y * self.speed

    #função para atualizar a posição da raquete
    def update(self):
        self.rect.y += self.speed
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1]))

    #função para desenhar a raquete
    def draw(self, screen):
        screen.blit(self.surface, self.rect)

#classe da bola
class Ball:
    #construtor da classe
    def __init__(self, size):
        self.size = size
        self.surface = pygame.Surface((size, size))
        self.surface.fill((255, 0, 0))
        self.rect = self.surface.get_rect()
        self.speed = [0, 0]
        self.reset()

    #função para resetar a bola
    def reset(self):
        self.rect.x = SCREEN_SIZE[0] / 2 - self.size / 2
        self.rect.y = SCREEN_SIZE[1] / 2 - self.size / 2
        self.speed = [random.choice([-1, 1]) * BALL_SPEED, random.choice([-1, 1]) * BALL_SPEED]

    #função para atualizar a posição da bola
    def update(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_SIZE[1]:
            self.speed[1] *= -1
        if self.rect.left <= 0 or self.rect.right >= SCREEN_SIZE[0]:
            self.speed[0] *= -1

    #função para verificar se a bola colidiu com a raquete
    def collide(self, paddle):
        if self.rect.colliderect(paddle.rect):
            self.speed[0] *= -1

    #função para desenhar a bola
    def draw(self, screen):
        screen.blit(self.surface, self.rect)

#classe para o placar
class Score:
    #construtor da classe
    def __init__(self):
        self.score = [0, 0]

    #função para atualizar o placar
    def update(self, player):
        self.score[player] += 1

    #função para resetar o placar
    def reset(self):
        self.score = [0, 0]

    #função para desenhar o placar
    def draw(self, screen):
        text = POINTS_FONT.render(str(self.score[0]) + ' x ' + str(self.score[1]), True, (255, 255, 255))
        screen.blit(text, (SCREEN_SIZE[0] / 2 - text.get_width() / 2, 10))

#função para desenhar os elementos na tela
def draw(screen, left_paddle, right_paddle, ball, score):
    screen.fill((0, 0, 0))
    left_paddle.draw(screen)
    right_paddle.draw(screen)
    ball.draw(screen)
    score.draw(screen)
    pygame.display.flip()

#função principal
def main():
    #inicialização das variáveis
    left_paddle = Paddle(PADDLE_SIZE, PADDLE_THICKNESS, LEFT_PADDLE_OFFSET, 0)
    right_paddle = Paddle(PADDLE_SIZE, PADDLE_THICKNESS, RIGHT_PADDLE_OFFSET, 0)
    ball = Ball(BALL_SIZE)
    score = Score()
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Pong")

    #loop principal
    running = True
    while running:
        clock.tick(30)
        #verificação de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            #verificação de teclas pressionadas
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r:
                    score.reset()
                    ball.reset()
                if event.key == pygame.K_w:
                    left_paddle.speed = -PADDLE_SPEED
                if event.key == pygame.K_s:
                    left_paddle.speed = PADDLE_SPEED
                if event.key == pygame.K_UP:
                    right_paddle.speed = -PADDLE_SPEED
                if event.key == pygame.K_DOWN:
                    right_paddle.speed = PADDLE_SPEED
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    left_paddle.speed = 0
                if event.key == pygame.K_s:
                    left_paddle.speed = 0
                if event.key == pygame.K_UP:
                    right_paddle.speed = 0
                if event.key == pygame.K_DOWN:
                    right_paddle.speed = 0

        #atualização dos elementos
        ball.collide(left_paddle)
        ball.collide(right_paddle)
        left_paddle.update()
        right_paddle.update()
        ball.update()
        if ball.rect.left <= 0:
            score.update(1)
            ball.reset()
        if ball.rect.right >= SCREEN_SIZE[0]:
            score.update(0)
            ball.reset()

        #desenho dos elementos
        draw(screen, left_paddle, right_paddle, ball, score)


#execução do programa
if __name__ == '__main__':
    main()

