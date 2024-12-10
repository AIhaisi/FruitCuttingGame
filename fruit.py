import pygame
import random

# 初始化 Pygame
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
# 设置屏幕尺寸
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("水果切割游戏")

# 定义分数
score = 0
background = pygame.image.load("Assets/background.png")

fruitsNum = 6
trail_color = (200, 200, 200)
trail_length = 15  # 轨迹长度

ballsNum = 2

explode_imgs = [pygame.image.load(f"Assets/explode/explode{i}.png") for i in range(1, 12)]

class Fruit:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(160, 640)
        self.y = 800
        self.pos = [self.x, self.y]

        self.speedx = random.randint(-10, 10)
        self.speedy = random.randint(-40, -30)
        self.vel = [self.speedx, self.speedy]

        self.radius = random.randint(80, 160)
        self.g = 1

        self.angle = 0
        self.left_angle = 0
        self.right_angle = 0

        self.url = "Assets/fruit/fruit" + str(random.randint(1, fruitsNum)) + ".png"
        self.image = pygame.image.load(self.url)
        self.image = pygame.transform.scale(self.image, (self.radius, self.radius))
        self.rect = self.image.get_rect(center=self.pos)

        self.split = False
        # 左半
        self.split_url1 = self.url.split(".")[0] + "_1.png"
        self.split_image1 = pygame.image.load(self.split_url1)
        self.split_image1 = pygame.transform.scale(self.split_image1, (self.radius, self.radius))
        # 右半
        self.split_url2 = self.url.split(".")[0] + "_2.png"
        self.split_image2 = pygame.image.load(self.split_url2)
        self.split_image2 = pygame.transform.scale(self.split_image2, (self.radius, self.radius))

        self.split_images = [pygame.transform.scale(self.split_image1, (self.radius, self.radius)),
                             pygame.transform.scale(self.split_image2, (self.radius, self.radius))]
        self.split_rects = [self.split_images[0].get_rect(center=self.pos),
                            self.split_images[1].get_rect(center=self.pos)]
        self.split_vels = [[random.choice([-15, -5]), random.choice([-10, 10])],
                           [random.choice([5, 15]), random.choice([-10, 10])]]
        self.juice_image = pygame.image.load("Assets/fruit/juice.png")
        self.juice_image = pygame.transform.scale(self.juice_image, (self.radius , self.radius ))
        self.juice_rect = self.juice_image.get_rect(center=self.pos)
        self.show_juice = False  # 是否显示爆汁效果
        self.juice_alpha = 255  # 爆汁效果的初始透明度
        self.juice_duration = 30  # 爆汁效果的持续时间（帧数）

    def update(self):
        if not self.split:
            self.pos[0] += self.vel[0]
            self.pos[1] += self.vel[1]
            self.vel[1] += self.g  # Gravity
            self.rect.center = self.pos

            self.angle += 5  # 增加旋转角度
            if self.angle >= 360:
                self.angle = 0

            if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
                self.vel[0] = -self.vel[0]

            if self.rect.bottom > 2 * SCREEN_HEIGHT:
                self.reset()
        else:
            self.left_angle += 5
            self.right_angle -= 5
            if self.left_angle >= 360:
                self.left_angle = 0  # 增加旋转角度
            if self.right_angle <= 0:
                self.right_angle = 360
            for i in range(2):
                self.split_rects[i].centerx += self.split_vels[i][0]
                self.split_rects[i].centery += self.split_vels[i][1]
                self.split_vels[i][1] += self.g  # Gravity

                if self.split_rects[i].left < 0 or self.split_rects[i].right > SCREEN_WIDTH:
                    self.split_vels[i][0] = -self.split_vels[i][0]

                if self.split_rects[i].bottom > 2 * SCREEN_HEIGHT + 400:
                    self.reset()
        if self.show_juice:
            # 如果显示爆汁效果，降低透明度并减少持续时间
            if self.juice_duration > 0:
                self.juice_duration -= 1
                self.juice_alpha = max(0, self.juice_alpha - 8)  # 每帧减少透明度
            else:
                self.show_juice = False  # 结束爆汁效果

    def draw(self):
        if self.split:
            if self.show_juice:  # 如果水果被切开且需要显示爆汁效果
                # 使用带有透明度的图像来绘制爆汁效果
                juice_image_with_alpha = self.juice_image.copy()
                juice_image_with_alpha.set_alpha(self.juice_alpha)
                screen.blit(juice_image_with_alpha, self.juice_rect)
        if not self.split:
            rotated_image = pygame.transform.rotate(self.image, self.angle)
            new_rect = rotated_image.get_rect(center=self.rect.center)
            screen.blit(rotated_image, new_rect.topleft)
        else:
            rotated_image1 = pygame.transform.rotate(self.split_image1, self.left_angle)
            rotated_image2 = pygame.transform.rotate(self.split_image2, self.right_angle)
            new_rect1 = rotated_image1.get_rect(center=self.split_rects[0].center)
            new_rect2 = rotated_image2.get_rect(center=self.split_rects[1].center)
            screen.blit(rotated_image1, new_rect1)
            screen.blit(rotated_image2, new_rect2)

    def mouse_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos) and not self.split:
            self.split = True
            self.left_angle = self.angle
            self.right_angle = self.angle
            global score
            score += 1
            self.show_juice = True  # 切开水果后显示爆汁效果
            self.juice_rect.center = self.rect.center  # 设置爆汁图像的位置
            self.juice_alpha = 255  # 重置透明度
            self.juice_duration = 30  # 重置持续时间
            for i in range(2):
                self.split_rects[i].center = self.rect.center
class Ball:
    def __init__(self):
        self.reset()
        self.show_score = False  # 是否显示分数
        self.score_alpha = 255  # 分数透明度
        self.score_pos = [0, 0]  # 分数位置
        self.score_timer = 0  # 分数显示计时器

    def reset(self):
        self.max_cuts = random.randint(3,5)  # 最大切割次数
        self.current_cuts = 0  # 当前切割次数
        self.last_cut_time = 0  # 上一次切割时间


        self.x = random.randint(160, 640)
        self.y = 800
        self.pos = [self.x, self.y]

        self.speedx = random.randint(-10, 10)
        self.speedy = random.randint(-40, -30)
        self.vel = [self.speedx, self.speedy]

        self.radius = random.randint(120, 200)
        self.g = 1

        self.angle = 0
        self.left_angle = 0
        self.right_angle = 0

        self.url = "Assets/ba/ba"+str(random.randint(1,ballsNum))+".png"
        self.image = pygame.image.load(self.url)
        self.image = pygame.transform.scale(self.image, (self.radius, self.radius))
        self.rect = self.image.get_rect(center=self.pos)

        self.exploded = False
        self.explode_index = 0
        self.explode_images = random.sample(explode_imgs, len(explode_imgs))


    def mouse_click(self, mouse_pos):
        current_time = pygame.time.get_ticks()
        if self.rect.collidepoint(mouse_pos) and self.current_cuts < self.max_cuts:
            if current_time - self.last_cut_time >= 200:  # 间隔 0.5 秒
                self.current_cuts += 1
                self.last_cut_time = current_time

                # 产生小位移
                self.vel[0] += random.choice([random.randint(-10, -5),random.randint(5,10)])
                self.vel[1] += random.randint(-5, -3)
                self.rect.center = self.pos



        if self.current_cuts == self.max_cuts:
            self.exploded = True


    def update(self):
        if not self.exploded:
            self.pos[0] += self.vel[0]
            self.pos[1] += self.vel[1]
            self.vel[1] += self.g  # Gravity
            self.rect.center = self.pos

            self.angle += 5  # 增加旋转角度
            if self.angle >= 360:
                self.angle = 0

            if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
                self.vel[0] = -self.vel[0]

            if self.rect.bottom > 2 * SCREEN_HEIGHT:
                self.reset()
        else:
            if self.explode_index < len(self.explode_images):
                self.explode_index += 1
            else:
                global score
                score += 10  # 增加分数
                self.show_score = True  # 切击时显示分数
                self.score_timer = 30  # 分数显示持续帧数（30帧）
                self.score_pos = list(self.rect.topleft)  # 分数显示在水果上方
                self.score_alpha = 255
                self.reset()
        if self.show_score:
            self.score_timer -= 1
            self.score_pos[1] -= 1  # 向上移动分数
            self.score_alpha -= 8  # 逐渐减少透明度
            if self.score_alpha <= 0 or self.score_timer <= 0:
                self.show_score = False  # 停止显示分数


    def draw(self):
        if not self.exploded:
            rotated_image = pygame.transform.rotate(self.image, self.angle)
            new_rect = rotated_image.get_rect(center=self.rect.center)
            screen.blit(rotated_image, new_rect.topleft)
        else:
            if self.explode_index < len(self.explode_images):
                screen.blit(self.explode_images[self.explode_index], self.rect.topleft)

        if self.show_score:
            font = pygame.font.Font(None, 72)
            score_text = font.render("+10", True, (125, 125, 255))
            score_text.set_alpha(self.score_alpha)  # 设置透明度
            screen.blit(score_text, self.score_pos)
def draw_trail(trail_points):
    if len(trail_points) > 1:
        # 逐段绘制渐变线
        for i in range(len(trail_points) - 1):
            # 计算当前段的宽度，从大到小
            start_width = max(5, int(10 * (1 - i / len(trail_points))))
            end_width = max(1, int(10 * (1 - (i + 1) / len(trail_points))))

            # 绘制线段，从 trail_points[i] 到 trail_points[i+1]
            pygame.draw.line(screen, trail_color, trail_points[i], trail_points[i + 1], start_width)
            pygame.draw.line(screen, trail_color, trail_points[i], trail_points[i + 1], end_width)


def game():
    global score
    score = 0
    fruits = [Fruit() for i in range(15)]
    balls = [Ball() for i in range(1)]
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)
    running = True
    mouse_held = False
    trail_points = []
    paused = False  # 是否暂停
    game_over = False
    pause_button_rect = pygame.Rect(SCREEN_WIDTH - 120, 10, 100, 50)
    while running:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_held = True
                if game_over:
                    mouse_pos = pygame.mouse.get_pos()
                    if restart_button_rect.collidepoint(mouse_pos):
                        game_over = False
                        score = 0
                        fruits = [Fruit() for i in range(15)]
                        balls = [Ball() for i in range(1)]
                elif pause_button_rect.collidepoint(pygame.mouse.get_pos()):
                    paused = not paused
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_held = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused

        if not game_over and not paused:
            if mouse_held:
                mouse_pos = pygame.mouse.get_pos()
                trail_points.append(mouse_pos)
                if len(trail_points) > trail_length:
                    trail_points.pop(0)
                for fruit in fruits:
                    fruit.mouse_click(mouse_pos)
                for ball in balls:
                    ball.mouse_click(mouse_pos)
            else:
                trail_points.clear()

            draw_trail(trail_points)

            for fruit in fruits:
                fruit.update()
                fruit.draw()
            for ball in balls:
                ball.update()
                ball.draw()

            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

            if score >= 200:
                game_over = True
        if paused:
            for fruit in fruits:
                fruit.draw()
            for ball in balls:
                ball.draw()
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

        if game_over:
            restart_button_rect = pygame.Rect(300, 250, 200, 50)
            pygame.draw.rect(screen, (255, 0, 0), restart_button_rect)
            restart_text = small_font.render("RESTART", True, (255, 255, 255))
            screen.blit(restart_text, (restart_button_rect.x + 50, restart_button_rect.y + 10))

        pygame.draw.rect(screen, (255, 255, 0), pause_button_rect)
        pause_text = small_font.render("PAUSE" if not paused else "START", True, (0, 0, 0))
        screen.blit(pause_text, (pause_button_rect.x + 10, pause_button_rect.y + 10))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()

def main_menu():
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)
    start_button_rect = pygame.Rect(300, 400, 200, 50)
    running = True

    while running:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        title_text = font.render("Fruit Cutting Game", True, (255, 255, 255))
        screen.blit(title_text, (150, 150))

        pygame.draw.rect(screen, (0, 255, 0), start_button_rect)
        start_text = small_font.render("START", True, (125, 0, 0))
        screen.blit(start_text, (start_button_rect.x + 55, start_button_rect.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_pos):
                    running = False

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    game()

if __name__ == "__main__":
    main_menu()
