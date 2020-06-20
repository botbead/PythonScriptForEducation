'''
Created by HuanyuWang at 2020-06-20

A script for testing keystroke and changing background color with keystroke.
'''

import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

keys_char_part = {
    46:'.',
    48:'0',
    49:'1',
    50:'2',
    51:'3',
    52:'4',
    53:'5',
    54:'6',
    55:'7',
    56:'8',
    57:'9',
    97:'a',
    98:'b',
    99:'c',
    100:'d',
    101:'e',
    102:'f',
    103:'g',
    104:'h',
    105:'i',
    106:'j',
    107:'k',
    108:'l',
    109:'m',
    110:'n',
    111:'o',
    112:'p',
    113:'q',
    114:'r',
    115:'s',
    116:'t',
    117:'u',
    118:'v',
    119:'w',
    120:'x',
    121:'y',
    122:'z',
    126:'`',
}

ypos_last = 0
xpos_last = 0
chars = []

words_count = 0

class Char(pygame.sprite.Sprite):

    def __init__(self, char, font):
        super(Char, self).__init__()
        self.char = char
        self.font = font
        self.surf = font.render(char, True, (0, 0, 0))
        self.rect = self.surf.get_rect()
        #if(self.char == ' '):
            #self.width = 3
        #else:
        self.width = self.surf.get_size()[0]
        self.height = self.surf.get_size()[1]
        self.update_global_pos()
        self.is_rookie = True

    def update_global_pos(self):
        global xpos_last,ypos_last
        if(xpos_last + self.width > (SCREEN_WIDTH-10)):
            xpos_last = 0
            self.rect.left = xpos_last
            ypos_last += self.height
            self.rect.top = ypos_last
        else:
            xpos_last += self.width
            self.rect.left = xpos_last
            self.rect.top = ypos_last
        self.is_rookie = False

    def update(self):
        pass

#lock = threading.Lock

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#(243,145,169)--->(124,184,14)
screen.fill((243,145,169))
font = pygame.font.SysFont("Consolas", 19)

Chars = pygame.sprite.Group()

clock = pygame.time.Clock()

temp_str = ""
sapce_index1 = 0
sapce_index2 = 0

exit = False
keyin_end = False

background_color_stack = []
background_color_stack.append((243,145,169))
key_hit_count_last = 0
key_hit_count = 0

while exit is not True:

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit = True
        elif event.type == pygame.QUIT:
            exit = True

    key_pressed = pygame.key.get_pressed()

    if key_pressed[pygame.K_SPACE]:
        if key_hit_count == 0:
            key_hit_count=1
        else:
            key_hit_count += 1
        c = Char(' ', font)
        Chars.add(c)
        if chars:
            if chars[len(chars)-1] != ' ':
                chars.append(' ')
        else:
            chars.append(' ')
    else:
        for k, v in keys_char_part.items():
            if key_pressed[k]:
                if key_hit_count ==0:
                    key_hit_count = 1
                else:
                    key_hit_count+=1
                c = Char(keys_char_part[k], font)
                Chars.add(c)
                chars.append(keys_char_part[k])
                if keys_char_part[k] == '.':
                    keyin_end = True

    if keyin_end:
        i = 0
        temp_str = ""
        while i < len(chars):
            if '.' == chars[i]:
                if temp_str.isalpha():
                    words_count += 1
                xpos_last = 0
                ypos_last += 20
                c = Char(str(words_count),font)
                Chars.add(c)
                ypos_last+=20
                c = Char('', font)
                Chars.add(c)
                temp_str = ""
                words_count = 0
                keyin_end = False
                chars.clear()
            elif ' ' == chars[i]:
                if ""!= temp_str:
                    if temp_str.isalpha():
                         words_count += 1
                temp_str = ""
            else:
                temp_str += chars[i]
            i+=1

    w = key_hit_count - key_hit_count_last
    key_hit_rate = (key_hit_count - key_hit_count_last) / 10.0
    key_hit_count_last = key_hit_count
    if 0 != w:
        if background_color_stack:
            x = background_color_stack[len(background_color_stack)-1][0] - ((background_color_stack[len(background_color_stack)-1][0] - 124) * key_hit_rate)
            if x < 124:
                x = 124
            y = background_color_stack[len(background_color_stack)-1][1] + ((background_color_stack[len(background_color_stack)-1][1] - 145) * key_hit_rate)
            if y > 184:
                y = 184
            z = background_color_stack[len(background_color_stack)-1][2] - ((background_color_stack[len(background_color_stack)-1][2] - 14) * key_hit_rate)
            if z < 14:
                z = 14
            screen.fill((x, y, z))
            background_color_stack.append((x, y, z))
    else:
        if len(background_color_stack) > 1:
            screen.fill(background_color_stack[len(background_color_stack) - 1])
            background_color_stack.pop()
        else:
            screen.fill(background_color_stack[0])


    for char in Chars:
        screen.blit(char.surf, char.rect)

    pygame.display.flip()
    clock.tick(30)


pygame.quit()