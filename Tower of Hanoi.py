import pygame

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0 ,0)
FPS = 60
size = (1100, 700)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
done = False

loop_height = 20

class loop_class():
    def __init__(self, center_pos, color, width):
        self.width = width
        self.height = loop_height
        self.center = list(center_pos)
        self.color = color
        self.bar = 0

    def show_loop(self):
        rect_value = (self.center[0]-self.width/2, self.center[1]-self.height/2, self.width, self.height)
        pygame.draw.rect(screen, self.color, rect_value)
        
    def detect_click(self, cursor_pos):
        top = self.center[1] - self.height/2
        bottom = self.center[1] + self.height/2
        left = self.center[0] - self.width/2
        right = self.center[0] + self.width/2

        if left <= cursor_pos[0] and cursor_pos[0] < right:
            if top <= cursor_pos[1] and cursor_pos[1] < bottom:
                return True
        return False

class bar_class():
    def __init__(self, center_pos):
        self.bar_size = [30, 250]
        self.board_size = [300, 40]
        self.bar_center = list(center_pos)
        self.board_top = self.bar_center[1]+self.bar_size[1]//2
        self.next_y = self.board_top - loop_height//2
        self.loop = []

    def show_bar(self):
        bar_rect_value = (self.bar_center[0]-self.bar_size[0]//2, self.bar_center[1]-self.bar_size[1]//2, \
                            self.bar_size[0], self.bar_size[1])
        board_rect_value = (self.bar_center[0]-self.board_size[0]//2, self.bar_center[1]+self.bar_size[1]//2, \
                            self.board_size[0], self.board_size[1])
        pygame.draw.rect(screen, (75, 75, 75), bar_rect_value)
        pygame.draw.rect(screen, (75, 75, 75), board_rect_value)

    def detect_click(self, cursor_pos):
        top = self.bar_center[1] - self.bar_size[1]//2
        bottom = self.bar_center[1] + self.bar_size[1]//2 + self.board_size[1]
        left = self.bar_center[0] - self.board_size[0]//2
        right = self.bar_center[0] + self.board_size[0]//2

        if left <= cursor_pos[0] and cursor_pos[0] < right:
            if top <= cursor_pos[1] and cursor_pos[1] < bottom:
                return True
        return False


loop_color = [(255, 0, 0), (255, 100, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (0, 0, 100), \
            (0, 255, 255), (100, 0, 100), (255, 0, 200), (255, 255, 255)]
loop = [0 for i in range(10)]
bar = [0 for i in range(3)]
move_to_cursor = [False, -1]

for i in range(len(loop)):
    c = 255-15*i
    loop[i] = loop_class((200, 10+loop_height*i), loop_color[i], 50+20*i)

for i in range(3):
    bar[i] = bar_class(((size[0]-200)//6+300*i+100, size[1]//2-40))

for i in range(0, 10):
    loop[9 - i].center[0] = bar[0].bar_center[0]
    loop[9 - i].center[1] = bar[0].next_y
    bar[0].loop.append(9-i)
    bar[0].next_y -= loop_height
    bar[0].top_loop = 0


while not done:
    clock.tick(FPS)
    screen.fill(BLACK)

    top_loop_num = []
    for i in range(3):
        try:
            top_loop_num.append(bar[i].loop[-1])
        except: pass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            cursor_pos = list(pygame.mouse.get_pos())
            for i in top_loop_num:
                if i == -1:
                    continue
                if loop[i].detect_click(cursor_pos) and not move_to_cursor[0]:
                    loop[i].center = cursor_pos
                    move_to_cursor = [True, i]
                    for i in bar:
                        if i.detect_click(cursor_pos):
                            i.next_y += loop_height
                            del i.loop[-1]
                    break
                elif move_to_cursor[0]:
                    move_to_cursor[0] = False
                    break
            
            if not move_to_cursor[0]:
                for j in range(len(bar)):
                    if bar[j].detect_click(cursor_pos) and move_to_cursor[1] != -1:
                        try:
                            if move_to_cursor[1] > bar[j].loop[-1]:
                                move_to_cursor[0] = True
                                break
                        except: pass
                        loop[move_to_cursor[1]].center[0] = bar[j].bar_center[0]
                        loop[move_to_cursor[1]].center[1] = bar[j].next_y
                        bar[j].next_y -= loop_height
                        bar[j].loop.append(move_to_cursor[1])
                        move_to_cursor[1] = -1
                for j in range(len(bar)):
                    if bar[j].detect_click(cursor_pos):
                        break
                    if j == 2:
                        move_to_cursor[0] = True
        
        if event.type == pygame.MOUSEMOTION and move_to_cursor[0]:
            cursor_pos = list(pygame.mouse.get_pos())
            loop[move_to_cursor[1]].center = cursor_pos
    
    for i in range(len(loop)):
        if move_to_cursor[0] and i == move_to_cursor[1]:
            continue
    
    for i in bar:
        i.show_bar()
    for i in loop:
        i.show_loop()
    
    pygame.display.update()

pygame.quit()