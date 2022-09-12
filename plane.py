import pygame as pg
from sys import exit
from random import choice
from data_screen import *
from pygame import event

# animasi pesawat
def animation():
    new_plane = plane_frames[plane_index]
    new_plane_rect = new_plane.get_rect(center = (50, plane_rect.centery))

    return new_plane, new_plane_rect

# rotasi dari pesawat
def rotate(img):
    new_plane = pg.transform.rotate(img, - plane_move * 3)
    return new_plane

# buat gedung
def create_building():
    random_building = choice(building_height)
    top_building = building.get_rect(midbottom = (DISPLAY_WIDTH + 26, random_building - 150))
    bottom_building = building.get_rect(midtop  = (DISPLAY_WIDTH + 26, random_building))

    return top_building, bottom_building

# implementasi gedung
def draw_building(buildings):
    for b in buildings:
        # jika gdung >= 512
        if b.bottom >= DISPLAY_HEIGHT:
            display.blit(building, b)
        else:
            flip_building = pg.transform.flip(building, False, True)
            display.blit(flip_building, b)

# perpindahan gedung
def move_building(buildings):
    for b in buildings:
        b.centerx -= 3
    return buildings

# munculin gedung
def spawn_building():
    if event.type == building_spawn:
        building_list.append(create_building())

# hapus gedung
def remove_building(buildings):
    global obstacle_number
    
    if len(buildings) != 0:
        if buildings[0][0] + 52 <= 0:
            buildings.pop(0)
            buildings.pop(0)
            obstacle_number -= 3
    
    return buildings[:]

# ground bergerak
def move_floor():
    display.blit(floor, (floor_pos_x, DISPLAY_HEIGHT - floor_rect.height // 2))
    display.blit(floor, (floor_pos_x + DISPLAY_WIDTH, DISPLAY_HEIGHT - floor_rect.height // 2))

# cek gedung lewat apa gak
def check_obstacle_passed():
    global obstacle_number
    buildings = building_list[:]

    if len(buildings) > obstacle_number:
        if buildings[obstacle_number][0] + 52 <= 26:
            obstacle_number  += 3
            point_snd.play()
            return True

    return False

# cek colision gedung
def check_collision(buildings):
    # jika pesawat nabrak gedung
    for b in buildings:
        if plane_rect.colliderect(b):
            collide_snd.play()
            return False

    if plane_rect.top <= 0 or plane_rect.bottom >= DISPLAY_HEIGHT - floor_rect.height // 2:
        collide_snd.play()
        return False;

    
    return True


# skor
def score_display(game_state):
    if game_state == "main_game":
        score_font = font.render(str(int(score)), True, white)
        score_font_rect = score_font.get_rect(center = (DISPLAY_WIDTH // 2, 50))
        display.blit(score_font, score_font_rect)
    elif game_state == "game_over":
        score_font = font.render(f'Score: {int(score)}', True, white)
        score_font_rect = score_font.get_rect(center = (DISPLAY_WIDTH // 2, 50))
        display.blit(score_font, score_font_rect)
        
        high_score_font = font.render(f'High Score : {int(high_score)}', True, white)
        high_score_font_rect = high_score_font.get_rect(center = (DISPLAY_WIDTH // 2, 412))
        display.blit(high_score_font, high_score_font_rect)

# tambah skor
def increment_score(scr, increment):
    if check_obstacle_passed():
        return scr + increment
    return scr

# update skor
def score_update(scr, high_scr):
    if scr > high_scr:
        high_scr = scr
    
    return high_scr

'DISPLAY'

# setting displaynya
display = pg.display.set_mode(DISPLAY_AREA)
pg.display.set_caption("Flappy Plane")

'BACKGROUND'
bg = pg.image.load('assets/images/sprites/bg-awan.png').convert()
floor = pg.image.load('assets/images/sprites/jalan-hd-revisi.png').convert_alpha()
floor_rect = floor.get_rect()
floor_pos_x = 0
building = pg.image.load('assets/images/sprites/gedung-1-hd-revisi.png')
building_list = []
building_spawn = pg.USEREVENT
obstacle_number = 0

pg.time.set_timer(building_spawn, 1200)
building_height = [200, 300, 400]

'PLANE'
plane_up = pg.image.load('assets/images/sprites/plane.png').convert_alpha()
plane_down = pg.image.load('assets/images/sprites/plane.png').convert_alpha()
plane_mid = pg.image.load('assets/images/sprites/plane.png').convert_alpha()
plane_frames = [plane_down, plane_mid, plane_up]
plane_index = 0
plane = plane_frames[plane_index]
plane_rect = plane.get_rect(center = (50, DISPLAY_HEIGHT // 2))
plane_flap = pg.USEREVENT + 1
pg.time.set_timer(plane_flap, 200)
plane_move = 0
gravity = 0.2

'SOUND EFFECT'
pg.mixer.init(44100, 16, 2, 512)
flap_snd = pg.mixer.Sound('assets/sounds/sound_effects/Flap.ogg')
collide_snd = pg.mixer.Sound('assets/sounds/sound_effects/Hit.ogg')
point_snd = pg.mixer.Sound('assets/sounds/sound_effects/Point.ogg')

'FONT'
pg.font.init()
font = pg.font.Font('assets/font/04B_19.ttf', 20)

'SCORE'
high_score = 0
score = high_score


'FPS'
# setting fps gamenya
clock = pg.time.Clock()
fps = 60

'LOPPING'
# gamenya
game = True
while True:
    clock.tick(fps)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE and game:
                plane_move = 0
                plane_move -= 6
            elif event.key == pg.K_SPACE and not game:
                game = True
                building_list.clear()
                plane_move = 0
                plane_rect.center = (50, DISPLAY_HEIGHT // 2)
                score = 0
                obstacle_number = 0

        if event.type == plane_flap:
            if plane_index < 2:
                plane_index += 1
            else:
                plane_index = 0
            
            plane, plane_rect = animation()

        if event.type == building_spawn:
            building_list.extend(create_building())

    display.blit(bg, (0, 0))

    if game:
        plane_move += gravity
        plane_rect.centery += int(plane_move)
        plane_rotate = rotate(plane)

        display.blit(plane_rotate, plane_rect)
        game = check_collision(building_list)

        # buat gedung
        draw_building(building_list)
        building_list = move_building(building_list)
        building_list = remove_building(building_list)

        # buat skor
        score_display('main_game')
        score = increment_score(score, 1)

    else:
        # display.blit(bg_game_over, bg_game_over_rect)
        
        # ambil data gedung
        building_list = move_building(building_list)
        building_list = remove_building(building_list)

        # ambil high score
        high_score = score_update(score, high_score)
        score_display('game_over')

    move_floor()
    if floor_pos_x <= -DISPLAY_WIDTH:
        floor_pos_x = 0
    floor_pos_x -= 1

    pg.display.update()


