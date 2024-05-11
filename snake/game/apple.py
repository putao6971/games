from random import randint
from snake.constant import *


class Apple:
    """
    苹果类：表示游戏中的苹果，蛇吃到苹果会增长身体长度。
    """

    def __init__(self, game):
        """
        初始化苹果对象。
        :param game: 游戏对象。
        """
        self.game = game
        self.x = self.y = 0  # 苹果的初始位置
        self.game.add_draw_action(self.draw)  # 将 draw 方法添加到游戏的绘制动作列表中
        self.drop()  # 生成一个新的苹果

    def drop(self):
        """
        生成一个新的苹果，确保苹果不在蛇的身体上。
        """
        snake = self.game.snake.body + [self.game.snake.head]  # 获取蛇的身体和头部的所有位置
        while True:
            (x, y) = randint(0, COLUMNS - 1), randint(0, ROWS - 1)  # 随机生成一个位置
            if (x, y) not in snake:  # 如果这个位置不在蛇的身体上
                self.x, self.y = x, y  # 将苹果的位置设置为这个位置
                break  # 退出循环

    def draw(self):
        """
        绘制苹果。
        """
        self.game.draw_cell(
            (self.x, self.y),  # 苹果的位置
            CELL_SIZE,  # 每个单元格的大小
            APPLE_COLOR_SKIN,  # 苹果的外框颜色
            APPLE_COLOR_BODY  # 苹果的主体颜色
        )
