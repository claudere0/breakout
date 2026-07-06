import pygame
from config import *
pygame.init()

class Paddle:
    def __init__(self):
        self.reset()

    def reset(self):
        self.width = 64
        self.height = 16
        self.x = int((WIDTH / 2) - (self.width / 2))
        self.y = int(HEIGHT - (self.height * 2))
        self.speed = 8
        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)
        self.direction = 0

    def update(self):
        self.direction = 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left >= 0:
            self.x -= self.speed
            self.direction = -1

        if keys[pygame.K_RIGHT] and self.rect.right <= WIDTH:
            self.x += self.speed
            self.direction = 1
        
        self.rect.x = int(self.x)

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

class Ball:
    def __init__(self, x, y):
        self.reset(x, y)
    
    def reset(self, x, y):
        self.speed_x = 4
        self.speed_y = -4
        self.max_speed = 8
        self.radius = 8
        self.rect = pygame.Rect(x, y, self.radius * 2, self.radius * 2)
        self.prev_rect = self.rect.copy()
    
    def update(self):
        self.prev_rect = self.rect.copy()
        
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def bounce(self, direction):
        if direction == 'x':
            self.speed_x *= -1
        elif direction == 'y':
            self.speed_y *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, CYAN, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)

class Brick:
    def __init__(self, x, y, health, width, height):
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.health = health
        self.colors = {4:BLUE, 3:GREEN, 2:YELLOW, 1:RED}
        self.is_alive = True
    
    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.is_alive = False

    def draw(self, screen):
        if not self.is_alive:
            return
        pygame.draw.rect(screen, self.colors[self.health], self.rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("breakout")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('monospace', 24)
        self.screen_color = BLACK

        self.paddle = Paddle()
        self.ball = Ball(int(WIDTH//2-WIDTH//64), int(WIDTH-(WIDTH//8))-16)
        self.select_level(1)
        self.create_bricks()

        self.state = MENU
        self.running = True

    def restart(self):
        self.paddle.reset()
        self.ball.reset(int(WIDTH//2-WIDTH//64), int(WIDTH-(WIDTH//8))-16)
        self.create_bricks()
        self.state = MENU

    def select_level(self, level):
        if level == 1:
            # "Chessboard"
            self.map = [
                [1,0,1,0,1,0,1,0],
                [0,1,0,1,0,1,0,1],
                [1,0,1,0,1,0,1,0],
                [0,1,0,1,0,1,0,1],
                [1,0,1,0,1,0,1,0],
                [0,1,0,1,0,1,0,1],
                [1,0,1,0,1,0,1,0],
                [0,1,0,1,0,1,0,1],
            ]

        elif level == 2:
            # "Pyramid" (Classic shape with increasing durability towards the top)
            self.map = [
                [0,0,0,3,3,0,0,0],
                [0,0,3,3,3,3,0,0],
                [0,2,2,2,2,2,2,0],
                [0,2,2,2,2,2,2,0],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
            ]

        elif level == 3:
            # "Columns" (Vertical lines allowing the ball to shoot straight to the top)
            self.map = [
                [4,0,3,0,3,0,4,0],
                [4,0,3,0,3,0,4,0],
                [2,0,2,0,2,0,2,0],
                [2,0,2,0,2,0,2,0],
                [1,0,1,0,1,0,1,0],
                [1,0,1,0,1,0,1,0],
                [1,0,1,0,1,0,1,0],
                [1,0,1,0,1,0,1,0],
            ]

        elif level == 4:
            # "Invader" (A fun pixel-art alien design)
            self.map = [
                [0,1,0,0,0,0,1,0],
                [0,0,1,0,0,1,0,0],
                [0,2,2,2,2,2,2,0],
                [2,2,0,2,2,0,2,2],
                [3,3,3,3,3,3,3,3],
                [0,3,3,3,3,3,3,0],
                [0,0,1,0,0,1,0,0],
                [0,1,0,0,0,0,1,0],
            ]

        elif level == 5:
            # "Fortress" (Your original fifth level with a strong roof and side gaps)
            self.map = [
                [4,4,4,4,4,4,4,4],
                [4,0,0,4,4,0,0,4],
                [3,0,0,3,3,0,0,3],
                [3,3,3,3,3,3,3,3],
                [2,2,0,2,2,0,2,2],
                [2,2,0,2,2,0,2,2],
                [1,1,0,0,0,0,1,1],
                [1,1,1,1,1,1,1,1],
            ]

        elif level == 6:
            # "Hourglass" (Narrows in the center, requires precise aiming)
            self.map = [
                [4,4,4,4,4,4,4,4],
                [0,3,3,3,3,3,3,0],
                [0,0,2,2,2,2,0,0],
                [0,0,0,1,1,0,0,0],
                [0,0,0,1,1,0,0,0],
                [0,0,2,2,2,2,0,0],
                [0,3,3,3,3,3,3,0],
                [4,4,4,4,4,4,4,4],
            ]

        elif level == 7:
            # "Maze" (An armored outer box with hidden paths and a weak bottom layer)
            self.map = [
                [4,4,4,4,4,4,4,4],
                [4,0,0,0,0,0,0,4],
                [4,0,3,3,3,3,0,4],
                [4,0,3,0,0,3,0,4],
                [4,0,3,0,0,3,0,4],
                [4,0,2,2,2,2,0,4],
                [0,0,0,0,0,0,0,0],
                [1,1,1,1,1,1,1,1],
            ]

        elif level == 8:
            # "Final Boss" (A dense and challenging grid with heavy armor)
            self.map = [
                [4,4,4,4,4,4,4,4],
                [4,4,4,4,4,4,4,4],
                [4,3,3,3,3,3,3,4],
                [3,3,2,2,2,2,3,3],
                [2,2,2,1,1,2,2,2],
                [1,1,1,0,0,1,1,1],
                [0,0,0,0,0,0,0,0],
                [1,0,1,0,0,1,0,1],
            ]

    def create_bricks(self):
        self.bricks = []

        brick_w = WIDTH // COLS
        brick_h = HEIGHT // 16

        for row, line in enumerate(self.map):
            for col, health in enumerate(line):
                if health == 0:
                    continue

                x = col * brick_w
                y = row * brick_h

                self.bricks.append(Brick(x, y, health, brick_w, brick_h))

    def bricks_collision(self):
        for brick in self.bricks:

            if not self.ball.rect.colliderect(brick.rect):
                continue

            self.resolve_collision(brick.rect)

            brick.hit()

            if not brick.is_alive:
                self.bricks.remove(brick)

            break

    def resolve_collision(self, rect):
        if self.ball.prev_rect.bottom <= rect.top:
            self.ball.rect.bottom = rect.top
            self.ball.bounce("y")
            return "top"

        elif self.ball.prev_rect.top >= rect.bottom:
            self.ball.rect.top = rect.bottom
            self.ball.bounce("y")
            return "bottom"

        elif self.ball.prev_rect.right <= rect.left:
            self.ball.rect.right = rect.left
            self.ball.bounce("x")
            return "left"

        elif self.ball.prev_rect.left >= rect.right:
            self.ball.rect.left = rect.right
            self.ball.bounce("x")
            return "right"

        return None

    def paddle_collision(self):
        if self.ball.rect.colliderect(self.paddle.rect):
            side = self.resolve_collision(self.paddle.rect)

            if side == "top":
                self.ball.speed_x += self.paddle.direction
                self.ball.speed_x = max(-self.ball.max_speed, min(self.ball.speed_x, self.ball.max_speed))

    def wall_collision(self):
        if self.ball.rect.right >= WIDTH:
            self.ball.rect.right = WIDTH
            self.ball.bounce('x')

        if self.ball.rect.left <= 0:
            self.ball.rect.left = 0
            self.ball.bounce('x')

        if self.ball.rect.top <= 0:
            self.ball.rect.top = 0
            self.ball.bounce('y')

    def handle_collisions(self):
        # screen
        self.wall_collision()

        # paddle
        self.paddle_collision()

        # bricks
        self.bricks_collision()

    def check_game_state(self):
        if self.ball.rect.bottom >= HEIGHT:
            self.state = LOSE
        
        if not self.bricks:
            self.state = WIN

    def update(self):
        if self.state != PLAYING:
            return
        self.paddle.update()
        self.ball.update()
        self.handle_collisions()
        self.check_game_state()

    def draw_text(self, text, x, y):
        text_image = self.font.render(text, True, WHITE)
        self.screen.blit(text_image, (x, y))

    def draw_bricks(self):
        for brick in self.bricks:
            brick.draw(self.screen)

    def draw_objects(self):
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        self.draw_bricks()

    def draw(self):
        self.screen.fill(self.screen_color)
        if self.state == PLAYING:
            self.draw_objects()
        elif self.state == MENU:
            self.draw_text("CHOOSE LEVEL", WIDTH//4+64, HEIGHT // 16 + 64)
            self.draw_text("PRESS BUTTON FROM 1 TO 8", WIDTH//8+64, HEIGHT // 8 + 64)
            self.draw_text("TO SELECT LEVEL", WIDTH//4+48, HEIGHT // 4 + 32)
        elif self.state == WIN:
            self.draw_text("YOU WON!", WIDTH//4+64, HEIGHT // 2 + 64)
            self.draw_text("PRESS R TO RESTART", WIDTH//8 + 32, HEIGHT // 2 + 96)
        elif self.state == LOSE:
            self.draw_text("YOU LOST!", WIDTH//4+64, HEIGHT // 2 + 64)
            self.draw_text("PRESS R TO RESTART", WIDTH//8 + 32, HEIGHT // 2 + 96)

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
                elif event.key == pygame.K_r:
                    self.restart()
                if self.state == MENU:
                    if event.key == pygame.K_1:
                        self.select_level(1)
                    elif event.key == pygame.K_2:
                        self.select_level(2)
                    elif event.key == pygame.K_3:
                        self.select_level(3)
                    elif event.key == pygame.K_4:
                        self.select_level(4)
                    elif event.key == pygame.K_5:
                        self.select_level(5)
                    elif event.key == pygame.K_6:
                        self.select_level(6)
                    elif event.key == pygame.K_7:
                        self.select_level(7)
                    elif event.key == pygame.K_8:
                        self.select_level(8)
                    else:
                        continue
                    self.create_bricks()
                    self.paddle.reset()
                    self.ball.reset(int(WIDTH//2-WIDTH//64), int(WIDTH-(WIDTH//8))-16)
                    self.state = PLAYING
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     if not self.live_ball:
            #         self.state = MENU

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()