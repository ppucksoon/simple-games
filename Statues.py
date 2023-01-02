import pygame
import time
import random

pygame.init()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0 ,0)
FPS = 60
size = (900, 600)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
done = False

font = pygame.font.Font('./font/NotoSansKR-Medium.otf', 30)

def playGame():
    global done
    playing = True
    rect_x = 10
    stop = True
    change_delay = True
    start_t = time.time()
    tagger_text = "무궁화 꽃이 피었습니다"
    tagger_index = 0
    delay = random.uniform(2, 5)
    play_time = 0
    start_play_time = time.time()

    while playing:
        clock.tick(FPS)
        screen.fill(BLACK)

        end_t = time.time()
        end_play_time = time.time()

        if not stop:
            if end_play_time - start_play_time >= 0.1:
                play_time += 0.1
                play_time = round(play_time, 1)
                start_play_time = time.time()
        else:
            start_play_time = time.time()

        if (not stop) and change_delay:
            delay = random.uniform(0.02, 0.5)
            change_delay = False
            tagger_index += 1

        if end_t - start_t >= delay:
            start_t = time.time()
            change_delay = True
            stop = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                done = True
            if event.type == pygame.KEYDOWN:
                rect_x += 1
                if stop:
                    print("실패")
                    playing = False

        if rect_x >= 830:
            print("성공")
            playing = False

        if tagger_index > 0:
            tagger = font.render(f"{tagger_text[:tagger_index]}", True, WHITE)
            tagger_center = tagger.get_rect()
            tagger_center.center = (450, 100)
            screen.blit(tagger, tagger_center)
        else:
            ready_text = font.render(f"준비", True, WHITE)
            ready_text_center = ready_text.get_rect()
            ready_text_center.center = (450, 100)
            screen.blit(ready_text, ready_text_center)

        if tagger_index == len(tagger_text)+1:
            stop = True
            delay = random.uniform(2, 5)
            start_t = time.time()
            change_delay = False
            tagger_index = 0

        last_time = font.render(f"{play_time}", True, WHITE)
        last_time_center = last_time.get_rect()
        last_time_center.center = (450, 550)
        screen.blit(last_time, last_time_center)
        pygame.draw.rect(screen, WHITE, (rect_x, 275, 50, 50))
        pygame.draw.rect(screen, RED, (880, 250, 5, 100))

        pygame.display.update()

def runGame():
    global done
    press_text = font.render("-시작하려면 아무 키나 누르세요-", True, WHITE)
    press_text_center = press_text.get_rect()
    press_text_center.center = (450, 500)

    while not done:
        clock.tick(FPS)
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    pass
                elif event.key == pygame.K_ESCAPE:
                    done = True
                else:
                    playGame()
        
        if time.time() % 1 > 0.5:
            screen.blit(press_text, press_text_center)
        pygame.display.update()

runGame()
pygame.quit()