import pygame
from config import *
from objects import *
pygame.init()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("breakout")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('monospace', 24)
        self.screen_color = BLACK

        self.paddle = Paddle()
        self.ball = Ball(int(WIDTH//2-WIDTH//64), int(WIDTH-(WIDTH//8))-16)
        self.level = 1
        self.build_level(1)
        self.create_bricks()

        self.state = MENU
        self.running = True

    def restart(self):
        self.state = MENU

    # alternative restart
    # def restart(self):
    #     self.start_level(self.level)

    def build_level(self, level):
        LEVELS = [
            # "Chessboard"
            [
                [1,0,1,0,1,0,1,0],
                [0,1,0,1,0,1,0,1],
                [1,0,1,0,1,0,1,0],
                [0,1,0,1,0,1,0,1],
                [1,0,1,0,1,0,1,0],
                [0,1,0,1,0,1,0,1],
                [1,0,1,0,1,0,1,0],
                [0,1,0,1,0,1,0,1],
            ],
            # "Pyramid" (Classic shape with increasing durability towards the top)
            [
                [0,0,0,3,3,0,0,0],
                [0,0,3,3,3,3,0,0],
                [0,2,2,2,2,2,2,0],
                [0,2,2,2,2,2,2,0],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
            ],
            # "Columns" (Vertical lines allowing the ball to shoot straight to the top)
            [
                [4,0,3,0,3,0,4,0],
                [4,0,3,0,3,0,4,0],
                [2,0,2,0,2,0,2,0],
                [2,0,2,0,2,0,2,0],
                [1,0,1,0,1,0,1,0],
                [1,0,1,0,1,0,1,0],
                [1,0,1,0,1,0,1,0],
                [1,0,1,0,1,0,1,0],
            ],
            # "Invader" (A fun pixel-art alien design)
            [
                [0,1,0,0,0,0,1,0],
                [0,0,1,0,0,1,0,0],
                [0,2,2,2,2,2,2,0],
                [2,2,0,2,2,0,2,2],
                [3,3,3,3,3,3,3,3],
                [0,3,3,3,3,3,3,0],
                [0,0,1,0,0,1,0,0],
                [0,1,0,0,0,0,1,0],
            ],
            # "Fortress" (Your original fifth level with a strong roof and side gaps)
            [
                [4,4,4,4,4,4,4,4],
                [4,0,0,4,4,0,0,4],
                [3,0,0,3,3,0,0,3],
                [3,3,3,3,3,3,3,3],
                [2,2,0,2,2,0,2,2],
                [2,2,0,2,2,0,2,2],
                [1,1,0,0,0,0,1,1],
                [1,1,1,1,1,1,1,1],
            ],
            # "Hourglass" (Narrows in the center, requires precise aiming)
            [
                [4,4,4,4,4,4,4,4],
                [0,3,3,3,3,3,3,0],
                [0,0,2,2,2,2,0,0],
                [0,0,0,1,1,0,0,0],
                [0,0,0,1,1,0,0,0],
                [0,0,2,2,2,2,0,0],
                [0,3,3,3,3,3,3,0],
                [4,4,4,4,4,4,4,4],
            ],
            # "Maze" (An armored outer box with hidden paths and a weak bottom layer)
            [
                [4,4,4,4,4,4,4,4],
                [4,0,0,0,0,0,0,4],
                [4,0,3,3,3,3,0,4],
                [4,0,3,0,0,3,0,4],
                [4,0,3,0,0,3,0,4],
                [4,0,2,2,2,2,0,4],
                [0,0,0,0,0,0,0,0],
                [1,1,1,1,1,1,1,1],
            ],
            # "Final" (A dense and challenging grid with heavy armor)
            [
                [4,4,4,4,4,4,4,4],
                [4,4,4,4,4,4,4,4],
                [4,3,3,3,3,3,3,4],
                [3,3,2,2,2,2,3,3],
                [2,2,2,1,1,2,2,2],
                [1,1,1,0,0,1,1,1],
                [0,0,0,0,0,0,0,0],
                [1,0,1,0,0,1,0,1],
            ]
        ]

        self.map = LEVELS[level-1]

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
        elif not self.bricks:
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
            self.draw_text("CHOOSE LEVEL", WIDTH//4+52, HEIGHT // 16 + 160)
            self.draw_text("PRESS BUTTON FROM 1 TO 8", WIDTH//8 + 32, HEIGHT // 8 + 160)
            self.draw_text("TO SELECT LEVEL", WIDTH//4+24, HEIGHT // 4 + 128)
            self.draw_text("OR Q TO QUIT", WIDTH//4+52, HEIGHT // 4 + 160)
        elif self.state == WIN:
            self.draw_objects()
            self.draw_text("YOU WON!", WIDTH//4+64, HEIGHT // 2 + 64)
            self.draw_text("PRESS R TO RESTART", WIDTH//8 + 32, HEIGHT // 2 + 96)
        elif self.state == LOSE:
            self.draw_objects()
            self.draw_text("YOU LOST!", WIDTH//4+70, HEIGHT // 2 + 64)
            self.draw_text("PRESS R TO RESTART", WIDTH//4, HEIGHT // 2 + 96)

        pygame.display.flip()

    def start_level(self, level):
        self.level = level
        self.build_level(level)
        self.create_bricks()
        self.paddle.reset()
        self.ball.reset(int(WIDTH//2-WIDTH//64), int(WIDTH-(WIDTH//8))-16)
        self.state = PLAYING

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
                elif event.key == pygame.K_r and self.state in (WIN, LOSE):
                    self.restart()
                if self.state == MENU:
                    if event.key == pygame.K_1:
                        self.start_level(1)
                    elif event.key == pygame.K_2:
                        self.start_level(2)
                    elif event.key == pygame.K_3:
                        self.start_level(3)
                    elif event.key == pygame.K_4:
                        self.start_level(4)
                    elif event.key == pygame.K_5:
                        self.start_level(5)
                    elif event.key == pygame.K_6:
                        self.start_level(6)
                    elif event.key == pygame.K_7:
                        self.start_level(7)
                    elif event.key == pygame.K_8:
                        self.start_level(8)
                    else:
                        continue

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