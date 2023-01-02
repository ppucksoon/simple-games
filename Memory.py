from functools import cache
from time import time
import pygame
import random
import copy

pygame.init()
pygame.display.set_caption("기억력 게임")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0 ,0)
FPS = 60
size = (450, 500)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
done = False

@cache
def font(size):
    return pygame.font.Font('./font/NotoSansKR-Medium.otf', size)

class rect_class():
    def __init__(self, scale, center, shrink):
        self.scale = list(copy.deepcopy(scale))
        self.center = list(copy.deepcopy(center))
        self.scale_ani = [True, 0]
        self.ani_color = [255, 255, 255]
        self.shrink = shrink

    def print_rect(self, color):
        x = self.center[0] - self.scale[0]/2
        y = self.center[1] - self.scale[1]/2
        pygame.draw.rect(screen, color, (x, y, self.scale[0], self.scale[1]))

    def animation(self):
        x = self.center[0] - self.scale[0]/2
        y = self.center[1] - self.scale[1]/2
        if self.scale_ani[0] and self.scale_ani[1] < self.shrink:
            self.scale[0] -= 1
            self.scale[1] -= 1
            self.scale_ani[1] += 1
            self.ani_color[0] -= 100//self.shrink
            self.ani_color[1] -= 100//self.shrink
            pygame.draw.rect(screen, self.ani_color, (x, y, self.scale[0], self.scale[1]))
            if self.scale_ani[1] == self.shrink:
                self.scale_ani[0] = False
                self.scale_ani[1] = 0
        elif not self.scale_ani[0] and self.scale_ani[1] < self.shrink:
            self.scale[0] += 1
            self.scale[1] += 1
            self.scale_ani[1] += 1
            self.ani_color[0] += 100//self.shrink
            self.ani_color[1] += 100//self.shrink
            pygame.draw.rect(screen, self.ani_color, (x, y, self.scale[0], self.scale[1]))
            if self.scale_ani[1] == self.shrink:
                self.scale_ani[0] = True
                self.scale_ani[1] = 0
                return False
        return True


def get_rect_num(mouse_pos):
    out_of_range = True
    for i in range(4):
        if mouse_pos[0] >= 110*i + 10 and mouse_pos[0] <= 110*(i+1):
            num = i
            for j in range(4):
                if mouse_pos[1] >= 110*j + 10 and mouse_pos[1] <= 110*(j+1):
                    num += 4*j
                    out_of_range = False
                    break
    if out_of_range:
        num = 16
    return num

def ready(state, max_score = 0):
    start = False

    get_new = True
    start_t = 0
    wait = False
    preview = []
    for i in range(4):
        for j in range(4):
            preview.append(rect_class((40, 40), (159 + 44*i, 51 + 44*j), 2))

    while not start:
        clock.tick(FPS)
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
                elif event.key == pygame.K_RETURN:
                    return False

        if state == "retry":
            start_txt = font(20).render("다시 시작하려면 ENTER 누르기", True, WHITE)
        else:
            start_txt = font(20).render("게임 시작하려면 ENTER 누르기", True, WHITE)

        if time() % 1 > 0.5:
            start_txt_center = start_txt.get_rect()
            start_txt_center.center = (size[0]/2, size[1]/2 + 50)
            screen.blit(start_txt, start_txt_center)

        title = font(30).render("기억력 게임", True, WHITE)
        title_center = title.get_rect()
        title_center.center = (size[0]/2, size[1]/2)
        screen.blit(title, title_center)

        mscore_txt = font(20).render(f"최고 기록 : {max_score}단계", True, WHITE)
        mscore_txt_center = mscore_txt.get_rect()
        mscore_txt_center.center = (size[0]/2, size[1] - 100)
        screen.blit(mscore_txt, mscore_txt_center)

        caution = font(15).render("최고기록은 저장되지 않습니다", True, WHITE)
        caution_center = caution.get_rect()
        caution_center.center = (size[0]/2, size[1] - 50)
        screen.blit(caution, caution_center)

        if get_new:
            show_index = random.randrange(16)
            get_new = False
        
        for i in range(16):
            preview[i].print_rect((255, 255, 255))
        if not get_new and not wait:
            wait = not preview[show_index].animation()
        
        if wait:
            if not start_t:
                start_t = time()
            if time() - start_t > 1:
                start_t = 0
                wait = False
                get_new = True


        pygame.display.update()

memory = []
max_score = 0
current_score = 0
correct = True
wrong = False
pressed = False
show = True
rest = True
buttons = []
count = 0
chosen_rect = 16

for i in range(4):
    for j in range(4):
        buttons.append(rect_class((100, 100), (60 + 110*j, 60 + 110*i), 5))

done = ready("start")

while not done:
    clock.tick(FPS)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not pressed and not show:
                mouse_pos = pygame.mouse.get_pos()
                chosen_rect = get_rect_num(mouse_pos)
                if chosen_rect >= 0 and chosen_rect <= 15:
                    pressed = True
                    if chosen_rect == memory[count]:
                        count += 1
                    else:
                        wrong = True
                    if count == len(memory):
                        correct = True
                        count = 0

    if not correct:
        for i in range(16):
            if not(pressed and i == chosen_rect):
                buttons[i].print_rect(WHITE)
    
    if correct:
        memory.append(random.randrange(16))
        current_score += 1
        start_t = time()
        show = True
        correct = False
    elif wrong:
        memory = []
        count = 0
        if current_score-1 > max_score:
            max_score = current_score-1
        current_score = 0
        pressed = False
        correct = True
        wrong = False
        done = ready("retry", max_score)

    if show and not pressed:
        for i in range(16):
            buttons[i].print_rect((200, 200, 200))
        if not rest:
            buttons[memory[count]].print_rect((155, 155, 255))
        
        if time() - start_t >= 0.1 and rest:
            rest = False
            start_t = time()
        if time() - start_t >= 1:
            rest = True
            count += 1
            start_t = time()

        if count == len(memory):
            show = False
            pressed = False
            count = 0

    if pressed:
        pressed = buttons[chosen_rect].animation()

    mscore_txt = font(20).render(f"최고 기록 : {max_score}단계", True, WHITE)
    mscore_txt_center = mscore_txt.get_rect()
    mscore_txt_center.center = (115, 475)
    screen.blit(mscore_txt, mscore_txt_center)

    cscore_txt = font(20).render(f"현재 기록 : {current_score}단계", True, WHITE)
    cscore_txt_center = cscore_txt.get_rect()
    cscore_txt_center.center = (335, 475)
    screen.blit(cscore_txt, cscore_txt_center)

    pygame.display.update()

pygame.quit()