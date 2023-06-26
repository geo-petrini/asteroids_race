import pygame
import pygame.mixer as mixer
import pygame.image as image
import math
import random
from loader import Loader

"""
REMEMBER
0;0 is top left
"""


loader = Loader(['resources',
                 'resources/fonts',
                 'resources/music',
                 'resources/sounds',
                 'resources/sprites'])


SHIP_SPRITES = []
ASTEROID_SPRITES = []
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
X = 0
Y = 1

def start_game():
    # Initialize Pygame
    pygame.init()
    pygame.display.set_icon(pygame.image.load(loader.get('icon.png')),)

    # Game window dimensions
    screen_width = 800
    screen_height = 1200

    # Create the game window
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Space race")

    # Sprite resources
    global SHIP_SPRITES
    global ASTEROID_SPRITES
    SHIP_SPRITES = load_sprites_sequence('ship (<#>).png', 1, 7)
    ASTEROID_SPRITES = load_sprites_sequence('asteroid (<#>).png', 1, 6)

    # Audio resources
    load_background_music()
    collision_sound = load_collision_sound()

    # Player dimensions
    player_width = 50
    player_height = 50

    # Enemy dimensions
    enemy_width = 50
    enemy_height = 50

    # Player
    player_ship_sprite = random.choice(SHIP_SPRITES)
    player_ship = init_sprite_object(player_ship_sprite, 'CENTER', 'BOTTOM')

    # Asteroids
    asteroids = []

    # Stars
    stars = []

    # Enemy starting position
    enemy_x = random.randint(0, screen_width - enemy_width)
    enemy_y = -enemy_height

    # Enemy speed
    enemy_speed = 5

    # Game loop
    running = True
    clock = pygame.time.Clock()

    score = 0
    highscore = score

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

        # Check if the music is not playing (e.g., due to an error or stopping condition)
        if not mixer.music.get_busy():
            mixer.music.play(-1)  # Restart the music if it stopped

        # Move the player
        update_ship(player_ship)
        update_asteroids(asteroids, score)
        update_stars(stars)
        

        # Check collision between player and asteroid
        #TODO destroy player and asteroid
        #TODO reset score
        #TODO enter new ship with effect
        # else increse score
        score += 1
        if score > highscore:
            highscore = score        


        # Draw the game objects
        screen.fill(BLACK)
        draw_sprite_object(stars, screen)
        draw_sprite_object(player_ship, screen)
        draw_sprite_object(asteroids, screen)
        draw_warning_indicators(asteroids, screen)
        draw_score(score, highscore, screen)
        # Update the game display
        pygame.display.flip()
        clock.tick(60)

    # Quit the game
    pygame.quit()


def load_sprites_sequence(name, min, max):
    """
    load sprites from filenames in a sequence identified by an iterator between min and max
    :param name: string with '<#>' as placeholder for iterator value
    """
    images = []
    for i in range(min, max):
        filename = name.replace('<#>', str(i))
        image = pygame.image.load(loader.get(filename))
        images.append(image)
    return images


def load_background_music():
    mixer.init()
    mixer.music.load(loader.get("space-120280.mp3"))
    mixer.music.set_volume(0.3)
    mixer.music.play(-1)  # -1 means loop indefinitely


def load_collision_sound():
    collision_sound = mixer.Sound(loader.get("collision.wav"))
    collision_sound.set_volume(0.75)
    return collision_sound


def init_sprite_object(sprite, x=None, y=None, x_speed=None, y_speed=None, scale=1, rotation=0):
    screen_width, screen_height = pygame.display.get_surface().get_size()
    obj = {}

    obj['sprite'] = sprite
    
    if scale != 1:
        size = obj['sprite'].get_size()
        scaled_sprite = pygame.transform.scale(sprite, (int(size[0]*scale), int(size[1]*scale)))
        obj['sprite'] = scaled_sprite

    if rotation != 0:
        size = obj['sprite'].get_size()
        rotated_sprite = pygame.transform.rotate(sprite, rotation)
        obj['sprite'] = rotated_sprite

    obj['x_speed'] = x_speed
    obj['y_speed'] = y_speed

    if isinstance(x, str):
        if x == 'LEFT':
            obj['x'] = 0
        if x == 'CENTER':
            obj['x'] = (screen_width - sprite.get_width()) // 2
        if x == 'RIGHT':
            obj['x'] = screen_width - sprite.get_width()
        if x == 'RANDOM':
            obj['x'] = random.randint(0, screen_width)
    if isinstance(x, int):
        obj['x'] = x

    if isinstance(y, str):
        if y == 'TOP':
            obj['y'] = 0
        if y == 'CENTER':
            obj['y'] = (screen_height - sprite.get_height()) // 2
        if y == 'BOTTOM':
            obj['y'] = screen_height - sprite.get_height()
        if y == 'RANDOM':
            obj['y'] = random.randint(0, screen_height)
    if isinstance(y, int):
        obj['y'] = y
    return obj


def update_ship(ship):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ship['x'] -= 5
    if keys[pygame.K_RIGHT]:
        ship['x'] += 5
    if keys[pygame.K_UP]:
        ship['y'] -= 5
    if keys[pygame.K_DOWN]:
        ship['y'] += 5

def update_asteroids(asteroids, score):
    max_factor = 45
    difficulty = math.pow(score, 1/30)
    screen_width, screen_height = pygame.display.get_surface().get_size()

    if random.randint(0, max_factor) == 1:   #TODO alter based on score
        asteroid = init_sprite_object(
            random.choice(ASTEROID_SPRITES),
            x='RANDOM',
            y=-200,
            y_speed=random.randint(7, math.floor(15*difficulty)),
            scale=random.random()*3,
            rotation = random.randint(0, 360))
        # ast.scale = 0.3
        asteroids.append(asteroid)
    for asteroid in asteroids:
        asteroid['y'] += asteroid['y_speed']
        if asteroid['y'] > screen_height+40:
            asteroids.remove(asteroid)

def update_stars(stars):
    screen_width, screen_height = pygame.display.get_surface().get_size()
    if len(stars) < 40:
        stars.append(init_sprite_object(
            pygame.image.load(loader.get('star.png')),
            x='RANDOM',
            y='TOP', y_speed=random.randint(10, 20),
            scale=random.random()*2))
    for star in stars:
        star['y'] += star['y_speed']
        if star['y'] > screen_height:
            stars.remove(star)

def draw_sprite_object(obj, screen):
    if not isinstance(obj, list):
        obj = [obj]
    for o in obj:
        screen.blit(o['sprite'], (o['x'], o['y']))

def draw_warning_indicators(asteroids, screen):
    # Draw warning indicators
    font = pygame.font.Font( loader.get('dogica.ttf'), 16)
    line_offset = 3
    for asteroid in asteroids:
        if asteroid['y'] < 0:
            warn_x = asteroid['x']+asteroid['sprite'].get_width()//2
            warn_y = 50
            text_surface = font.render('WARNING', True, RED)
            text_rect = text_surface.get_rect()
            text_rect.center = (warn_x, warn_y)
            
            # pygame.draw.rect(screen, RED, (warn_x, warn_y, 10, 5))
            screen.blit(text_surface, text_rect)
            pygame.draw.line(screen, RED, (text_rect.topleft[X]-line_offset, text_rect.topleft[Y]-line_offset), (text_rect.topright[X], text_rect.topright[Y]-line_offset))
            pygame.draw.line(screen, RED, (text_rect.bottomleft[X]-line_offset, text_rect.bottomleft[Y]+line_offset), (text_rect.bottomright[X], text_rect.bottomright[Y]+line_offset))

def draw_score(score, highscore, screen):
    offset = 3
    screen_width, screen_height = pygame.display.get_surface().get_size()
    font = pygame.font.Font( loader.get('dogica.ttf'), 8)    
    text_surface = font.render(f'Score: {score} | Highscore: {highscore}', True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.bottomleft = (0+offset, screen_height-offset)
    screen.blit(text_surface, text_rect)

if __name__ == '__main__':
    start_game()
