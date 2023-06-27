import pygame
import pygame.mixer as mixer
import pygame.image as image
import math
import random
from modules.loader import Loader
from modules.texthelper import TextRenderer
from modules.positionhelper import get_window_size
from modules.positionhelper import calc_x_textual_position
from modules.positionhelper import calc_y_textual_position
from modules.gameobject import GameObject
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
MUSIC_VOLUME = 0.3


def start_game():
    # Initialize Pygame
    pygame.init()
    pygame.display.set_icon(pygame.image.load(loader.get('icon.png')),)

    # Game window dimensions
    screen_width = 800
    screen_height = 1000
    display_info = pygame.display.Info()

    screen_width = display_info.current_w if display_info.current_w < screen_width else screen_width
    screen_height = display_info.current_h if display_info.current_h < screen_height else screen_height

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
    # player_ship = init_sprite_object(player_ship_sprite, 'CENTER', 'BOTTOM')
    player_ship = GameObject(player_ship_sprite, ('CENTER', 'BOTTOM'))

    # Asteroids
    asteroids = []
    asteroids_group = pygame.sprite.Group()

    # Stars
    stars = []

    # Enemy starting position
    enemy_x = random.randint(0, screen_width - enemy_width)
    enemy_y = -enemy_height

    # Enemy speed
    enemy_speed = 5

    # Game loop
    running = True
    paused = False
    clock = pygame.time.Clock()

    score = 0
    highscore = score
    difficulty = 1

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                paused = not paused
            if keys[pygame.K_q]:
                running = False

        # Check if the music is not playing (e.g., due to an error or stopping condition)
        if not mixer.music.get_busy():
            mixer.music.play(-1)  # Restart the music if it stopped

        # Move the player
        if not paused:
            difficulty = update_difficulty(score)
            update_ship(player_ship)
            update_asteroids(asteroids, asteroids_group, difficulty)
            update_stars(stars)

        # Check collision between player and asteroid
        # TODO destroy player and asteroid
        # TODO reset score
        # TODO enter new ship with effect
        # else increse score
        # if pygame.sprite.spritecollide(player_ship, asteroids_group, False, pygame.sprite.collide_mask):
        #     draw_text('HIT')

        if score > highscore:
            highscore = score

        # Draw the game objects
        screen.fill(BLACK)
        draw_sprite_object(stars, screen)

        if score < 60:
            draw_jump_in(screen)
        else:
            draw_sprite_object(player_ship, screen)
        draw_sprite_object(asteroids, screen)
        draw_warning_indicators(asteroids, screen)
        # draw_score(score, highscore, screen)
        draw_text([f'Score: {score}',
                   f'Highscore: {highscore}',
                   f'Clock: {clock}',
                   f'Paused: {paused}'
                   ], screen)

        if paused:
            draw_pause(screen)
            mixer.music.set_volume(0.1)
        else:
            mixer.music.set_volume(MUSIC_VOLUME)

        # Update the game display
        pygame.display.flip()
        clock.tick(60)
        score += 1

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
    mixer.music.set_volume(MUSIC_VOLUME)
    mixer.music.play(-1)  # -1 means loop indefinitely


def load_collision_sound():
    collision_sound = mixer.Sound(loader.get("collision.wav"))
    collision_sound.set_volume(0.75)
    return collision_sound

def update_difficulty(score):
    return math.pow(score, 1/20)

def update_ship(ship):
    screen_width, screen_height = get_window_size()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ship.x -= 5
    if keys[pygame.K_RIGHT]:
        ship.x += 5
    if keys[pygame.K_UP]:
        ship.y -= 5
    if keys[pygame.K_DOWN]:
        ship.y += 5


def update_asteroids(asteroids, asteroids_group, difficulty):
    max_factor = 45
    screen_width, screen_height = get_window_size()

    if random.randint(0, max_factor) < 2*difficulty:
        # asteroid = init_sprite_object(
        #     random.choice(ASTEROID_SPRITES),
        #     x='RANDOM',
        #     y=-200,
        #     y_speed=random.randint(7, math.floor(15*difficulty)),
        #     scale=random.random()*3,
        #     rotation = random.randint(0, 360))
        # ast.scale = 0.3

        asteroid = GameObject(random.choice(ASTEROID_SPRITES),
                              position=('RANDOM', -200),
                              scale=random.random()*3)
        asteroid.y_speed = random.randint(7, math.floor(15*difficulty))
        asteroids.append(asteroid)
        # asteroids_group.add(asteroid.sprite)

    for asteroid in asteroids:
        asteroid.y += asteroid.y_speed
        if asteroid.y > screen_height+40:
            asteroids.remove(asteroid)


def update_stars(stars):
    screen_width, screen_height = get_window_size()
    if len(stars) < 40:
        # stars.append(init_sprite_object(
        #     pygame.image.load(loader.get('star.png')),
        #     x='RANDOM',
        #     y='TOP', y_speed=random.randint(10, 20),
        #     scale=random.random()*2))
        star = GameObject( pygame.image.load(loader.get('star.png')),
                          position = ('RANDOM', 'TOP'),
                          scale=random.random()*2)
        star.y_speed=random.randint(10, 20)
        stars.append(star)
    for star in stars:
        star.y += star.y_speed
        if star.y > screen_height:
            stars.remove(star)


def draw_sprite_object(obj, screen):
    if not isinstance(obj, list):
        obj = [obj]
    for o in obj:
        o.render(screen)


def draw_warning_indicators(asteroids, screen):
    # Draw warning indicators
    screen_width, screen_height = get_window_size()
    font = pygame.font.Font(loader.get('dogica.ttf'), 16)
    line_offset = 3
    for asteroid in asteroids:
        if asteroid.y < 0:
            warn_x = asteroid.x+asteroid.sprite.get_width()//2
            warn_y = 50
            text_surface = font.render('WARNING', True, RED)
            text_rect = text_surface.get_rect()
            text_rect.center = (warn_x, warn_y)

            # move if out of bounds
            if text_rect.x < 0:
                text_rect.x = 0
            if text_rect.topright[X] > screen_width:
                text_rect.x = screen_width - text_rect.width

            # pygame.draw.rect(screen, RED, (warn_x, warn_y, 10, 5))
            screen.blit(text_surface, text_rect)
            pygame.draw.line(screen, RED, (text_rect.topleft[X]-line_offset, text_rect.topleft[Y] -
                             line_offset), (text_rect.topright[X], text_rect.topright[Y]-line_offset))
            pygame.draw.line(screen, RED, (text_rect.bottomleft[X]-line_offset, text_rect.bottomleft[Y] +
                             line_offset), (text_rect.bottomright[X], text_rect.bottomright[Y]+line_offset))


def draw_text(text, screen):
    tr = TextRenderer(pygame.font.Font(loader.get('dogica.ttf'), 8))
    tr.lines = text
    tr.position = (TextRenderer.LEFT, TextRenderer.BOTTOM)
    tr.margin = 5
    tr.render(screen)


def draw_pause(screen):
    tr = TextRenderer(pygame.font.Font(loader.get('dogica.ttf'), 32))
    tr.lines = 'PAUSE'
    tr.position = (TextRenderer.CENTER, TextRenderer.CENTER)
    tr.margin = 5
    tr.render(screen)


def draw_jump_in(screen):
    screen_width, screen_height = get_window_size()

    for i in range(15):
        offset_from_center = random.randint(-40, 40)
        default_lenght = random.randint(200, 240)
        alpha = 100 - abs(offset_from_center)  # fade farther from center
        # shorter farther from center
        lenght = default_lenght - math.floor(abs(offset_from_center*1.7))

        bottom_point = (screen_width//2 + offset_from_center,
                        screen_height - (default_lenght - lenght)//2)
        top_point = (screen_width//2 + offset_from_center,
                     screen_height - default_lenght + (default_lenght - lenght)//2)

        # pygame.draw.line(screen, WHITE, start_point, end_point)
        vertical_line = pygame.Surface((4, lenght), pygame.SRCALPHA)
        vertical_line.fill((255, 255, 255, alpha))
        screen.blit(vertical_line, top_point)

# region(collapsed) deprecated code


def DEPRECATED_init_sprite_object(sprite, x=None, y=None, x_speed=None, y_speed=None, scale=1, rotation=0):
    screen_width, screen_height = get_window_size()
    obj = {}

    obj['sprite'] = sprite

    if scale != 1:
        size = obj['sprite'].get_size()
        scaled_sprite = pygame.transform.scale(
            sprite, (int(size[0]*scale), int(size[1]*scale)))
        obj['sprite'] = scaled_sprite

    if rotation != 0:
        size = obj['sprite'].get_size()
        rotated_sprite = pygame.transform.rotate(sprite, rotation)
        obj['sprite'] = rotated_sprite

    obj['x_speed'] = x_speed
    obj['y_speed'] = y_speed

    if isinstance(x, str):
        obj['x'] = calc_x_textual_position(x, screen_width, sprite.get_width())
    if isinstance(x, int):
        obj['x'] = x

    if isinstance(y, str):
        obj['y'] = calc_y_textual_position(
            y, screen_height, sprite.get_height())

    if isinstance(y, int):
        obj['y'] = y
    return obj

# endregion


if __name__ == '__main__':
    start_game()
