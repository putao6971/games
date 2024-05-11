import pygame
from pygame.locals import *
import random


# 定义砖块类
class Brick:
    def __init__(self, position, color):
        # 初始化砖块的位置和颜色
        self.position = position
        self.color = color
        # 创建一个与砖块大小相同的图像
        self.image = pygame.Surface([brick_width, brick_height])
        # 用砖块的颜色填充图像
        self.image.fill(self.color)

    # 绘制砖块
    def draw(self):
        # 将砖块图像绘制到屏幕上
        screen.blit(self.image, (self.position[0] * brick_width, self.position[1] * brick_height))


# 定义方块类
class Block:
    def __init__(self, bricks_layout, direction, color):
        # 初始化方块的布局、方向和颜色
        self.bricks_layout = bricks_layout
        self.direction = direction
        self.current_layout = self.bricks_layout[self.direction]
        self.position = current_block_init_position
        self.stopped = False
        self.move_interval = 800
        self.bricks = []
        # 根据当前布局和颜色创建方块的砖块
        for (x, y) in self.current_layout:
            self.bricks.append(Brick(
                (self.position[0] + x, self.position[1] + y),
                color))

    # 设置方块的位置
    def set_position(self, position):
        self.position = position
        self.refresh_bricks()

    # 绘制方块
    def draw(self):
        # 绘制方块的所有砖块
        for brick in self.bricks:
            brick.draw()

    # 检查新位置是否合法
    @staticmethod
    def is_legal(layout, position):
        (x0, y0) = position
        for (x, y) in layout:
            # 如果新位置超出游戏区域或与已有砖块重叠，则不合法
            if x + x0 < 0 or y + y0 < 0 or x + x0 >= field_width or y + y0 >= field_height:
                return False
            if field_map[y + y0][x + x0] != 0:
                return False
        return True

    # 向左移动方块
    def move_left(self):
        new_position = (self.position[0] - 1, self.position[1])
        if self.is_legal(self.current_layout, new_position):
            self.position = new_position
            self.refresh_bricks()

    # 向右移动方块
    def move_right(self):
        new_position = (self.position[0] + 1, self.position[1])
        if self.is_legal(self.current_layout, new_position):
            self.position = new_position
            self.refresh_bricks()

    # 向下移动方块
    def move_down(self):
        (x, y) = (self.position[0], self.position[1] + 1)
        while self.is_legal(self.current_layout, (x, y)):
            self.position = (x, y)
            self.refresh_bricks()
            y += 1

    # 更新方块的砖块位置
    def refresh_bricks(self):
        for (brick, (x, y)) in zip(self.bricks, self.current_layout):
            brick.position = (self.position[0] + x, self.position[1] + y)

    # 停止方块并添加到游戏区域
    def stop(self):
        global field_bricks
        global score
        self.stopped = True
        ys = []
        for brick in self.bricks:
            field_bricks.append(brick)
            (x, y) = brick.position
            if y not in ys:
                ys.append(y)
            # 将砖块添加到游戏区域地图中
            field_map[y][x] = 1

        eliminate_count = 0
        ys.sort()
        for y in ys:
            if 0 in field_map[y]:
                continue
            eliminate_count += 1
            # 消除一行，将上面的行向下移动
            for fy in range(y, 0, -1):
                field_map[fy] = field_map[fy - 1][:]
            field_map[0] = [0 for _ in range(field_width)]

            # 更新消除行上方的砖块位置
            tmp_field_bricks = []
            for fb in field_bricks:
                (fx, fy) = fb.position
                if fy < y:
                    fb.position = (fx, fy + 1)
                    tmp_field_bricks.append(fb)
                elif fy > y:
                    tmp_field_bricks.append(fb)
            field_bricks = tmp_field_bricks
        # 根据消除的行数增加分数
        if eliminate_count == 1:
            score += 1
        elif eliminate_count == 2:
            score += 2
        elif eliminate_count == 3:
            score += 4
        elif eliminate_count == 4:
            score += 6

    # 更新方块的状态
    def update(self, c_time):
        global last_move
        self.draw()
        # 如果达到下落时间间隔，则尝试向下移动方块
        if last_move == -1 or c_time - last_move >= self.move_interval:
            new_position = (self.position[0], self.position[1] + 1)
            if self.is_legal(self.current_layout, new_position):
                self.position = new_position
                self.refresh_bricks()
                last_move = c_time
            else:
                self.stop()

    # 旋转方块
    def rotate(self):
        new_direction = (self.direction + 1) % len(self.bricks_layout)
        new_layout = self.bricks_layout[new_direction]
        if not self.is_legal(new_layout, self.position):
            return
        self.direction = new_direction
        self.current_layout = new_layout
        for (brick, (x, y)) in zip(self.bricks, self.current_layout):
            brick.position = (self.position[0] + x, self.position[1] + y)
        self.refresh_bricks()
        self.draw()


# 绘制游戏区域的砖块
def draw_field():
    for brick in field_bricks:
        brick.draw()


# 绘制信息面板
def draw_info_panel():
    font = pygame.font.Font("resources/fonts/MONACO.TTF", 18)
    survived_text = font.render('Score: ' + str(score), True, (255, 255, 255))
    text_rect = survived_text.get_rect()
    # noinspection SpellCheckingInspection
    text_rect.topleft = ((field_width + 2) * brick_width, 10)
    screen.blit(survived_text, text_rect)

    next_block.draw()


# 绘制游戏区域的边框
def draw_frame():
    frame_color = pygame.Color(200, 200, 200)
    pygame.draw.line(screen, frame_color, (field_width * brick_width, field_height * brick_height),
                     (field_width * brick_width, 0), 3)


# 随机生成一个方块
def get_block():
    block_type = random.randint(0, 6)
    if block_type == 0:
        return Block(bricks_layout_0, random.randint(0, len(bricks_layout_0) - 1), colors_for_bricks[0])
    elif block_type == 1:
        return Block(bricks_layout_1, random.randint(0, len(bricks_layout_1) - 1), colors_for_bricks[1])
    elif block_type == 2:
        return Block(bricks_layout_2, random.randint(0, len(bricks_layout_2) - 1), colors_for_bricks[2])
    elif block_type == 3:
        return Block(bricks_layout_3, random.randint(0, len(bricks_layout_3) - 1), colors_for_bricks[3])
    elif block_type == 4:
        return Block(bricks_layout_4, random.randint(0, len(bricks_layout_4) - 1), colors_for_bricks[4])
    elif block_type == 5:
        return Block(bricks_layout_5, random.randint(0, len(bricks_layout_5) - 1), colors_for_bricks[5])
    elif block_type == 6:
        return Block(bricks_layout_6, random.randint(0, len(bricks_layout_6) - 1), colors_for_bricks[6])


# 方块布局定义
# 0: oooo
# 1: oo
#    oo
# 2: o
#   ooo
# 3: o
#    oo
#     o
# 4:  o
#    oo
#    o
# 5: ooo
#    o
# 6: ooo
#      o
bricks_layout_0 = (
    ((0, 0), (0, 1), (0, 2), (0, 3)),
    ((0, 1), (1, 1), (2, 1), (3, 1)))
bricks_layout_1 = (
    ((1, 0), (2, 0), (1, 1), (2, 1)),
)
bricks_layout_2 = (
    ((1, 0), (0, 1), (1, 1), (2, 1)),
    ((0, 1), (1, 0), (1, 1), (1, 2)),
    ((1, 2), (0, 1), (1, 1), (2, 1)),
    ((2, 1), (1, 0), (1, 1), (1, 2)),
)
bricks_layout_3 = (
    ((0, 1), (1, 1), (1, 0), (2, 0)),
    ((0, 0), (0, 1), (1, 1), (1, 2)),
)
bricks_layout_4 = (
    ((0, 0), (1, 0), (1, 1), (2, 1)),
    ((1, 0), (1, 1), (0, 1), (0, 2)),
)
bricks_layout_5 = (
    ((0, 0), (1, 0), (1, 1), (1, 2)),
    ((0, 2), (0, 1), (1, 1), (2, 1)),
    ((1, 0), (1, 1), (1, 2), (2, 2)),
    ((2, 0), (2, 1), (1, 1), (0, 1)),
)
bricks_layout_6 = (
    ((2, 0), (1, 0), (1, 1), (1, 2)),
    ((0, 0), (0, 1), (1, 1), (2, 1)),
    ((0, 2), (1, 2), (1, 1), (1, 0)),
    ((2, 2), (2, 1), (1, 1), (0, 1)),
)

# 方块颜色定义
colors_for_bricks = (
    pygame.Color(255, 0, 0), pygame.Color(0, 255, 0), pygame.Color(0, 0, 255),
    pygame.Color(100, 100, 100), pygame.Color(120, 200, 0), pygame.Color(100, 0, 200),
    pygame.Color(10, 100, 30))

# 游戏区域大小
field_width, field_height = 12, 17
# 当前方块的初始位置
current_block_init_position = (4, 0)
# 信息面板宽度
info_panel_width = 8
# 下一个方块的初始位置
next_block_init_position = (field_width + 3, 5)
# 游戏区域地图，0表示无砖块，1表示有砖块
field_map = [[0 for i in range(field_width)] for j in range(field_height)]

# 游戏结束图像
game_over_img = pygame.image.load("resources/images/game_over.gif")

# 游戏是否在运行
running = True
# 当前分数
score = 0
# 砖块大小
brick_width, brick_height = 30, 30
# 游戏区域的砖块列表
field_bricks = []

# 下一个方块
next_block = None
# 上次移动时间
last_move = -1

# 初始化pygame
pygame.init()
# 创建屏幕
screen = pygame.display.set_mode(((field_width + info_panel_width) * brick_width, field_height * brick_height), 0, 32)
# 设置游戏标题
pygame.display.set_caption('stormsha Tetris')

# 主游戏循环
while running:
    # 如果下一个方块不存在，则生成一个新方块
    if next_block is None:
        current_block = get_block()
    else:
        current_block = next_block
        current_block.set_position(current_block_init_position)
    # 生成下一个方块
    next_block = get_block()
    next_block.set_position(next_block_init_position)

    # 如果新方块的位置不合法，则游戏结束
    if not current_block.is_legal(current_block.current_layout, current_block.position):
        current_block.draw()
        running = False
        continue
    # 当前方块没有停止时，不断更新其状态
    while not current_block.stopped:
        # 清空屏幕
        screen.fill(0)
        # 绘制游戏区域边框
        draw_frame()
        # 获取当前时间
        time = pygame.time.get_ticks()
        # 更新当前方块的状态
        current_block.update(time)
        # 绘制游戏区域的砖块
        draw_field()
        # 绘制信息面板
        draw_info_panel()

        # 更新屏幕
        pygame.display.flip()
        pygame.display.update()
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # 退出游戏
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == K_w or event.key == K_UP:
                    # 旋转方块
                    current_block.rotate()
                    last_move = time
                elif event.key == K_a or event.key == K_LEFT:
                    # 向左移动方块
                    current_block.move_left()
                elif event.key == K_d or event.key == K_RIGHT:
                    # 向右移动方块
                    current_block.move_right()
                elif event.key == K_s or event.key == K_DOWN:
                    # 向下移动方块
                    current_block.move_down()
                    last_move = time - 500

# 游戏结束后，显示游戏结束图像
screen.blit(game_over_img, (field_width / 2 * brick_width, (field_height / 2 - 2) * brick_height))

# 等待玩家退出游戏
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    # 更新屏幕
    pygame.display.flip()
    pygame.display.update()
