from functools import cache
import pygame
import time
import random

pygame.init()
pygame.display.set_caption("Snake")

WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLACK = (0, 0 ,0)
HEAD = (0, 200, 0)
BODY = (100, 200, 100)
APPLE = (200, 0, 0)

FPS = 60
size = (470, 500)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

done = False

@cache
def font(size):
    return pygame.font.Font('./font/NotoSansKR-Medium.otf', size)

rect_len = 20
gap = 2
score = 0

def abs_coord(x, y):
    return [(rect_len + gap)*x + 5, (rect_len + gap)*y + 5]

class Snake():
    def __init__(self):
        self.x = 10
        self.y = 10
        self.direc = "stop"
        self.body = [[self.x, self.y]]

    def move(self):
        for i in range(len(self.body)-1):
            self.body[len(self.body)-i-1] = self.body[len(self.body)-i-2]
        self.body[0] = [self.x, self.y]

        if self.direc == "right":
            self.x += 1
        elif self.direc == "left":
            self.x -= 1
        elif self.direc == "up":
            self.y -= 1
        elif self.direc == "down":
            self.y += 1

        if self.x < 0 or self.x > 20 or self.y < 0 or self.y > 20:
            return True
        if len(snake.body) > 1:
            for i in self.body:
                if i[0] == self.x and i[1] == self.y:
                    return True
        return False

    def show(self):
        for i in self.body:
            coord = abs_coord(i[0], i[1])
            pygame.draw.rect(screen, BODY, (coord[0], coord[1], rect_len, rect_len))
        coord = abs_coord(self.x, self.y)
        pygame.draw.rect(screen, HEAD, (coord[0], coord[1], rect_len, rect_len))

class Apple():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def show(self):
        coord = abs_coord(self.x, self.y)
        pygame.draw.rect(screen, APPLE, (coord[0], coord[1], rect_len, rect_len))

apple = Apple(random.randint(0, 20), random.randint(0, 20))
snake = Snake()

def show():
    for i in range(21):
        for j in range(21):
            pygame.draw.rect(screen, GRAY, ((rect_len+gap)*j + 5, (rect_len+gap)*i + 5, rect_len, rect_len))

    snake.show()
    apple.show()

    text_txt = font(20).render(f"score : {score}", True, WHITE)
    text_txt_center = text_txt.get_rect()
    text_txt_center.center = (size[0]//2, 480)
    screen.blit(text_txt, text_txt_center)

start_t = time.time()
is_moved = True
game_over = False

while not done:
    clock.tick(FPS)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and is_moved:
            if event.key == pygame.K_ESCAPE:
                done = True
            elif event.key == pygame.K_RIGHT and snake.direc != "left":
                snake.direc = "right"
            elif event.key == pygame.K_LEFT and snake.direc != "right":
                snake.direc = "left"
            elif event.key == pygame.K_UP and snake.direc != "down":
                snake.direc = "up"
            elif event.key == pygame.K_DOWN and snake.direc != "up":
                snake.direc = "down"
            is_moved = False

    if time.time() - start_t >= 0.3:
        game_over = snake.move()
        start_t = time.time()
        is_moved = True

    if game_over:
        snake = Snake()
        apple = Apple(random.randint(0, 20), random.randint(0, 20))
        start_t = time.time()
        is_moved = True
        score = 0
        game_over = False

    if snake.x == apple.x and snake.y == apple.y:
        apple.x = random.randint(0, 20)
        apple.y = random.randint(0, 20)
        snake.body.append([-10, -10])
        score += 1

    show()

    pygame.display.update()

pygame.quit()