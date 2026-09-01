import pygame
import pygame._freetype as freetype

pygame.init()
freetype.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('P-shooter')

# clock controls frame rate
clock = pygame.time.Clock()
FPS = 60

# fonts for drawing text on screen (big for title, small for hints)
font_big = freetype.Font(None, 60)
font_small = freetype.Font(None, 28)

x = 200
y = 200

# how fast the soldier moves, in pixels per second
SPEED = 250
# gravity pulls the soldier down, in pixels/second^2
GRAVITY = 800
# how fast he rockets up when he jumps
JUMP_SPEED = 380

# a list of platforms. each is a rectangle: (x, y, width, height)
# pygame rectangles use TOP-LEFT corner for x,y
platforms = [
    pygame.Rect(0, 540, 800, 100),   # the big ground across the bottom (y=540 down to bottom)
    pygame.Rect(300, 440, 200, 20),  # a ledge in the middle
    pygame.Rect(150, 330, 200, 20),  # a higher ledge
]

# a pea bullet - one class = the blueprint for every bullet
class Pea(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed):
        super().__init__()
        # a small round green circle is our pea - big & bright so we can see it fly!
        self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (100, 200, 50), (8, 8), 7)
        pygame.draw.circle(self.image, (180, 255, 140), (8, 8), 3)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction   # 1 = right, -1 = left
        self.speed = speed

    # called every frame to move the bullet
    def update(self, dt):
        self.rect.x += self.speed * self.direction * dt

# a zombie plant - same blueprint idea as a pea, but it has health and shambles
class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y, health=3):
        super().__init__()
        self.image = pygame.Surface((50, 70))
        # a creepy green blob with a red eye
        pygame.draw.ellipse(self.image, (60, 130, 40), self.image.get_rect())
        pygame.draw.circle(self.image, (200, 40, 40), (25, 20), 6)  # red eye
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.health = 3
        self.speed = 40

    # slow shambles toward the soldier
    def update(self, dt, soldier_rect):
        if self.rect.centerx < soldier_rect.centerx:
            self.rect.x += self.speed * dt
        elif self.rect.centerx > soldier_rect.centerx:
            self.rect.x -= self.speed * dt

img = pygame.image.load('images/soldier.png')
# the source image is huge (900x1050) - shrink it to a good on-screen size
img = pygame.transform.scale(img, (60, 70))
rect = img.get_rect()
rect.center = (x, y)

# the title screen picture, stretched to fill the window
menu_img = pygame.image.load('images/Idle.png')
menu_img = pygame.transform.scale(menu_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# which part of the game we're in: 'menu' or 'play'
state = 'menu'

# his up/down speed; starts at 0 (standing still vertically)
velocity_y = 0
# is he standing on something? (starts false, platforms will set it true)
on_ground = False
# has the player won? (all zombies dead)
mission_complete = False

# a group (a bag) that holds all the peas flying around
peas = pygame.sprite.Group()
# which way the soldier faces: 1 = right, -1 = left
facing = 1

# a group that holds all the zombie plants
zombies = pygame.sprite.Group()
zombies.add(Zombie(650, 480))
zombies.add(Zombie(450, 390))
zombies.add(Zombie(250, 290))

running = True

while running:
    # time delta means how many secnds since last frame: this make the game run at same speed on fast and slow computers
    dt = clock.tick(FPS) / 1000.0

    # ---------- MENU (title) SCREEN ----------
    if state == 'menu':
        # draw the title picture full screen
        screen.blit(menu_img, (0, 0))
        title_surf, title_rect = font_big.render("P-SHOOTER", (255, 255, 255))
        title_rect.center = (SCREEN_WIDTH // 2, 120)
        screen.blit(title_surf, title_rect)
        start_surf, start_rect = font_small.render("Press ENTER to start your mission", (255, 255, 0))
        start_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        screen.blit(start_surf, start_rect)
        controls_surf, controls_rect = font_small.render("Arrows move & jump   Space shoots peas", (0, 0, 0))
        controls_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)
        screen.blit(controls_surf, controls_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                state = 'play'   # start the mission!

        pygame.display.update()
        continue   # skip the rest of this frame - we're in the menu

    # fills the screen with sky blue background
    screen.fill((135, 206, 235))
    # draw each platform as a brown rectangle
    for platform in platforms:
        pygame.draw.rect(screen, (139, 90, 43), platform)
    zombies.draw(screen)
    # draw a little health bar over each zombie
    for zombie in zombies:
        bar = pygame.Rect(zombie.rect.x, zombie.rect.y - 8, 50, 6)
        pygame.draw.rect(screen, (200, 40, 40), bar)                    # red = lost health
        green = int(50 * zombie.health / 3)
        pygame.draw.rect(screen, (80, 200, 80), (bar.x, bar.y, green, 6))  # green = remaining
    peas.draw(screen)
    screen.blit(img, rect)

    # get_pressed() returns which keys are held down
    keys = pygame.key.get_pressed()

    # left and right arrows move the soldier
    if keys[pygame.K_LEFT]:
        rect.x -= SPEED * dt
        facing = -1   # now facing left
    if keys[pygame.K_RIGHT]:
        rect.x += SPEED * dt
        facing = 1    # now facing right

    # jump when up arrow pressed AND he's on the ground
    if keys[pygame.K_UP] and on_ground:
        velocity_y = -JUMP_SPEED   # negative = up
        on_ground = False

    # gravity makes his fall speed grow every frame
    velocity_y += GRAVITY * dt
    rect.y += velocity_y * dt

    # check every platform for a landing
    on_ground = False
    for platform in platforms:
        # are his feet hitting the top of a platform, and is he falling?
        if rect.colliderect(platform) and velocity_y > 0:
            # snap his feet to the platform top and stop falling
            rect.bottom = platform.top
            velocity_y = 0
            on_ground = True

    # hold SPACE to keep shooting - fire while the key is held down
    if keys[pygame.K_SPACE]:
        pea = Pea(rect.centerx, rect.centery, facing, 300)
        peas.add(pea)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and mission_complete:
            # restart: put back all zombies, clear peas, reset
            zombies = pygame.sprite.Group()
            zombies.add(Zombie(650, 480))
            zombies.add(Zombie(450, 390))
            zombies.add(Zombie(250, 290))
            peas = pygame.sprite.Group()
            mission_complete = False

    # move every pea, then drop the ones that flew off screen
    peas.update(dt)
    for pea in list(peas):
        if pea.rect.right < 0 or pea.rect.left > SCREEN_WIDTH:
            peas.remove(pea)

    # move the zombies toward the soldier
    zombies.update(dt, rect)

    # did any pea hit any zombie?
    hits = pygame.sprite.groupcollide(zombies, peas, False, True)
    for zombie in hits:
        zombie.health -= 1
        if zombie.health <= 0:
            zombie.kill()

    # check if all zombies are dead
    if len(zombies) == 0 and not mission_complete:
        mission_complete = True

    # show the win message on top of everything
    if mission_complete:
        text_surf, text_rect = font_big.render("MISSION COMPLETE!", (0, 200, 0))
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        screen.blit(text_surf, text_rect)
        restart_surf, restart_rect = font_small.render("Press R to play again", (255, 255, 255))
        restart_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)
        screen.blit(restart_surf, restart_rect)

    pygame.display.update()

pygame.quit()
