import pygame

from snake import constant


class Snake:
    """贪吃蛇"""

    def __init__(self, game):
        self.game = game
        self.sound_hit = pygame.mixer.Sound("resources/hit.wav")
        self.sound_eat = pygame.mixer.Sound("resources/eat.wav")
        self.game.add_draw_action(self.draw)

        # 初始化数据
        self.head = (constant.SNAKE_X, constant.SNAKE_Y)  # 蛇头当前位置
        self.body = [(-1, -1)] * constant.SNAKE_BODY_LENGTH  # 蛇身长度
        self.direction = constant.SNAKE_DIRECTION  # 当前方向
        self.new_direction = constant.SNAKE_DIRECTION  # 移动方向
        self.speed = constant.SNAKE_SPEED  # 移动速度
        self.is_alive = True  # 是否存活

    def set_speed(self, speed):
        """
        @summary: 设置蛇的移动速度
        :param speed: 移动速度
        :return:
        """
        self._speed = speed
        self.game.add_game_action("snake.move", self.move, 1000 // speed)

    def get_speed(self):
        """
        @summary: 获取当前蛇的移动速度
        :return:
        """
        return self._speed

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        self._speed = speed
        self.game.add_game_action("snake.move", self.move, 1000 // speed)

    def draw(self):
        """
        @summary: 绘制小蛇
        :return: 
        """
        skin_color = constant.SNAKE_COLOR_SKIN if self.is_alive else constant.SNAKE_COLOR_SKIN_DEAD
        body_color = constant.SNAKE_COLOR_BODY if self.is_alive else constant.SNAKE_COLOR_BODY_DEAD
        head_color = constant.SNAKE_COLOR_HEAD if self.is_alive else constant.SNAKE_COLOR_HEAD_DEAD
        for cell in self.body:
            self.game.draw_cell(cell, constant.CELL_SIZE, skin_color, body_color)
        self.game.draw_cell(self.head, constant.CELL_SIZE, skin_color, head_color)

    def turn(self, direction):
        """
        @summary: 改变小蛇方向
        :param direction: 
        :return: 
        """
        if (self.direction in (constant.LEFT, constant.RIGHT) and direction in (constant.UP, constant.DOWN) or
                self.direction in (constant.UP, constant.DOWN) and direction in (constant.LEFT, constant.RIGHT)):
            self.new_direction = direction

    def move(self):
        """
        @summary: 移动小蛇
        :return: 
        """
        if not self.is_alive:
            return
        # 设定方向
        self.direction = self.new_direction
        # 检测前方
        x, y = meeting = (
            self.head[0] + self.direction[0],
            self.head[1] + self.direction[1]
        )
        # 死亡判断
        if meeting in self.body or x not in range(constant.COLUMNS) or y not in range(constant.ROWS):
            self.die()
            return
        # 判断是否吃了苹果
        if meeting == (self.game.apple.x, self.game.apple.y):
            self.sound_eat.play()
            self.game.apple.drop()
            self.game.apple_count += 1
        else:
            self.body.pop()
        # 蛇头变成脖子
        self.body = [self.head] + self.body
        # 蛇头移动到新位置
        self.head = meeting

    def restart_pawn(self):
        """重生"""
        self.head = (constant.SNAKE_X, constant.SNAKE_Y)
        self.body = [(-1, -1)] * constant.SNAKE_BODY_LENGTH
        self.direction = constant.SNAKE_DIRECTION
        self.new_direction = constant.SNAKE_DIRECTION
        self.speed = constant.SNAKE_SPEED
        self.is_alive = True

    def die(self):
        self.sound_hit.play()
        self.is_alive = False
