import pygame
from pygame.locals import *
import random, math, sys, time
pygame.init()

clock = pygame.time.Clock()

surface = pygame.display.set_mode((1200,600)) # określenie płaszczyzny rysowania
pygame.display.set_caption('ZFWPG: Projekt, model bez tarcia') # tytuł na pasku

# zmienne globalne
g = 9.81
a = 0
squares = []
n = 0
f = 0
v_value = 0
start_time = 0
paused = False

# kolory
COLOR_INACTIVE = pygame.Color('lightskyblue3') # niekatywne pole tekstowe
COLOR_ACTIVE = pygame.Color('red') # aktywne pole tekstowe
COLOR_BG = pygame.Color('white') # tło
COLOR_ARROW = pygame.Color('black') # kolor strzałki

# czcionki
FONT = pygame.font.Font(None, 32)

# etykiety
info = FONT.render("", 1, (0,0,255))
label_n = FONT.render("Ilość obiektów:", 1, (0,0,255))
label_f = FONT.render("Siła F:", 1, (0,0,255))
label_f_unit = FONT.render("N", 1, (0,0,255))
label_m = FONT.render("Masy kolejnych obiektów:", 1, (0,0,255))
label_powers = FONT.render("Siły działające na kolejne ciała:", 1, (0,0,255))
label_v = FONT.render("Prędkość ciał:", 1, (0,0,255))
label_v_value = FONT.render("{0:.2f}".format(v_value) + " m/s", 1, (0,0,255))
label_a = FONT.render("Wartość przyspieszenia:", 1, (0,0,255))
label_a_value = FONT.render("{0:.2f}".format(a) + " m/s^2", 1, (0,0,255))
label_t = FONT.render("Czas:", 1, (0,0,255))
label_t_value = FONT.render("{0:.2f}".format(0) + " s", 1, (0,0,255))

labels_p = []
labels_m = []
for i in range(12):
    labels_m.append(FONT.render("", 1, (0,0,255)))

def reset():
    global a
    global squares
    global n
    global f
    global v_value
    global start_time
    global paused
    global input_boxes
    global labels_m
    global label_v_value
    global label_a_value
    global label_t_value
    a = 0
    squares = []
    n = 0
    f = 0
    v_value = 0
    start_time = 0
    paused = False
    input_boxes = input_boxes[:4]
    input_boxes[0].text = ""
    input_boxes[0].txt_surface = FONT.render("", True, input_boxes[0].color)
    input_boxes[1].text = ""
    input_boxes[1].txt_surface = FONT.render("", True, input_boxes[1].color)
    labels_m = []
    for i in range(12):
        labels_m.append(FONT.render("", 1, (0,0,255)))
    label_v_value = FONT.render("{0:.2f}".format(v_value) + " m/s", 1, (0,0,255))
    label_a_value = FONT.render("{0:.2f}".format(a) + " m/s^2", 1, (0,0,255))
    label_t_value = FONT.render("{0:.2f}".format(0) + " s", 1, (0,0,255))
    
class InputBox:

    def __init__(self, x, y, w, h, text='', label=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.label = label
        self.active = False

    def handle_event(self, event):
        
        global paused
        global input_boxes
        global squares
        global n
        global f
        global info
        global labels_m
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                if self.label == "stop":
                    paused = not paused
                    if paused:
                        input_boxes[2].text = "START"
                        input_boxes[2].txt_surface = FONT.render("START", True, COLOR_INACTIVE)
                    else:
                        input_boxes[2].text = "STOP"
                        input_boxes[2].txt_surface = FONT.render("STOP", True, COLOR_INACTIVE)
                elif self.label == "reset":
                    reset()
                else:
                    self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if self.label == 'n':
                        n = int(self.text)
                        if n > 6:
                            info = info = FONT.render("Nie można rysować więcej niż 6 obiektów.", 1, (0,0,255))
                        else:
                            info = info = FONT.render("", 1, (0,0,255))
                            squares = []
                            input_boxes = input_boxes[:4]
                            labels_m = []
                            for i in range(12):
                                labels_m.append(FONT.render("", 1, (0,0,255)))
                            for i in range(n):
                                squares.append(Square((random.randint(0,255), random.randint(0,255), random.randint(0,255)), 0, 50+i*100))
                                input_boxes.append(InputBox(500, 150 + i * 50, 140, 32, label='m'+str(i)))
                                labels_m[i] = FONT.render("m"+str(i)+":", 1, (0,0,255))
                                labels_m[i+6] = FONT.render("kg", 1, (0,0,255))
                    if self.label == 'f':
                        f = float(self.text)
                    if self.label == 'm0':
                        squares[0].mass = float(self.text)
                    if self.label == 'm1':
                        squares[1].mass = float(self.text)
                    if self.label == 'm2':
                        squares[2].mass = float(self.text)
                    if self.label == 'm3':
                        squares[3].mass = float(self.text)
                    if self.label == 'm4':
                        squares[4].mass = float(self.text)
                    if self.label == 'm5':
                        squares[5].mass = float(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

# lista pól tekstowych
input_boxes = [InputBox(500, 50, 140, 32, label='n'), InputBox(500, 100, 140, 32, label='f'), InputBox(780, 255, 140, 32, label='stop'), InputBox(780, 305, 140, 32, label='reset')]
input_boxes[2].text = "STOP"
input_boxes[2].txt_surface = FONT.render("STOP", True, input_boxes[2].color)
input_boxes[3].text = "RESET"
input_boxes[3].txt_surface = FONT.render("RESET", True, input_boxes[3].color)

class Square:
    def __init__(self, color, mass, x, y = 100, w = 100, h = 100):
        self.shape = pygame.Rect(x, 600 - y, w, h)
        self.color = color
        self.mass = mass

def move():
    global a
    global squares
    global v_value
    global label_v_value
    global label_a_value
    global label_t_value
    global start_time
    if f != 0 and len(squares) > 0:
        for s in squares:
            if s.mass == 0:
                break
        else:
            if start_time == 0:
                start_time = time.time()
            m_sum = 0
            for s in squares:
                m_sum += s.mass
            a = f / m_sum
            label_a_value = FONT.render("{0:.2f}".format(a) + " m/s^2", 1, (0,0,255))
            v_value += a/58
            print(squares[-1].shape.x)
            for s in squares:
                label_v_value = FONT.render("{0:.2f}".format(v_value) + " m/s", 1, (0,0,255))
                label_t_value = FONT.render("{0:.2f}".format(time.time() - start_time) + " s", 1, (0,0,255))
                s.shape.move_ip(v_value, 0)
                
def draw():
    """
    Funkcja rysująca na ekranie.
    """
    
    surface.fill(COLOR_BG) # kolor tła
    
    for box in input_boxes:
        box.update()
    for box in input_boxes:
        box.draw(surface)

    surface.blit(label_n, (60, 55))
    surface.blit(label_f, (60, 105))
    surface.blit(label_f_unit, (720, 105))
    surface.blit(label_m, (60, 155))
    for i in range(6):
        surface.blit(labels_m[i], (450, 155 + i * 50))
        surface.blit(labels_m[i+6], (720, 155 + i * 50))
    #surface.blit(FONT.render("{0:.2f}".format(circles[0].radius/100), 1, (0,0,255)), (400, 155))
    surface.blit(info, (80, 455))

    surface.blit(label_v, (780, 55))
    surface.blit(label_v_value, (940, 55))
    surface.blit(label_a, (780, 105))
    surface.blit(label_a_value, (1060, 105))
    surface.blit(label_t, (780, 155))
    surface.blit(label_t_value, (860, 155))

    #pygame.draw.polygon(surface, (0, 0, 0), ((0, 100), (0, 200), (200, 200), (200, 300), (300, 150), (200, 0), (200, 100)))

    for s in squares:
        pygame.draw.rect(surface, s.color, s.shape)

    if len(squares) > 0 and f > 0:
        line_start = (squares[-1].shape.x + squares[-1].shape.width, squares[-1].shape.y + squares[-1].shape.height/2)
        line_end = (squares[-1].shape.x + squares[-1].shape.width + (f * 10), squares[-1].shape.y + squares[-1].shape.height/2)
        triangle_up = (squares[-1].shape.x + squares[-1].shape.width + (f * 10) - 6, squares[-1].shape.y + squares[-1].shape.height/2 + 6)
        triangle_down = (squares[-1].shape.x + squares[-1].shape.width + (f * 10) - 6, squares[-1].shape.y + squares[-1].shape.height/2 - 6)
        pygame.draw.line(surface, COLOR_ARROW, line_start, line_end, 3)
        pygame.draw.polygon(surface, COLOR_ARROW, [line_end, triangle_up, triangle_down], 4)

    pygame.display.flip()
    
def get_input():
    """
    Funkcja pozwalająca na przechwycenie interakcji.
    """
    
    keystate = pygame.key.get_pressed()
    
    for event in pygame.event.get():

        for box in input_boxes:
            box.handle_event(event)
            
        if event.type == QUIT or keystate[K_ESCAPE]:
            #print("--- %s seconds ---" % (time.time() - start_time))
            #print("v: " + str(v_value))
            pygame.quit()
            sys.exit()
            
def main():
    while True:
        clock.tick(60)
        get_input()
        if not paused:
            move()
        draw()
    
if __name__ == '__main__':
    main()
