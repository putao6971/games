from snake.game.apple import Apple  # 导入苹果类
from snake.game.base import *  # 导入游戏基类
from snake.game.snake import Snake  # 导入蛇类


class SnakeGame(GameBase):
    """贪吃蛇游戏"""

    def __init__(self):
        """初始化游戏"""
        super(SnakeGame, self).__init__(
            game_name=GAME_NAME, icon=ICON,  # 调用基类的初始化方法
            screen_size=SCREEN_SIZE,
            display_mode=DISPLAY_MODE,
            loop_speed=LOOP_SPEED,
            font_size=FONT_SIZE,
            background=WHITE,
            font_name=None
        )
        # 绘制背景
        self.prepare_background()
        # 创建游戏对象
        self.apple_count = 0  # 苹果计数器
        self.high_score = 0  # 记录最高分
        self.snake = Snake(self)  # 创建蛇对象
        self.apple = Apple(self)  # 创建苹果对象
        # 绑定按键事件
        self.add_key_binding(KEY_UP, self.snake.turn, direction=UP)  # 绑定上方向键
        self.add_key_binding(KEY_DOWN, self.snake.turn, direction=DOWN)  # 绑定下方向键
        self.add_key_binding(KEY_LEFT, self.snake.turn, direction=LEFT)  # 绑定左方向键
        self.add_key_binding(KEY_RIGHT, self.snake.turn, direction=RIGHT)  # 绑定右方向键
        self.add_key_binding(KEY_RESTART, self.restart)  # 绑定R键（重启游戏）
        self.add_key_binding(KEY_PAUSE, self.pause)  # 绑定R键（重启游戏）
        self.add_key_binding(KEY_EXIT, self.quit)  # 绑定退出键
        # 添加绘图函数
        self.add_draw_action(self.draw_score)  # 添加绘制分数的函数

    def prepare_background(self):
        """准备背景"""
        self.background.fill(BACKGROUND_COLOR)  # 用背景颜色填充背景
        for _ in range(CELL_SIZE, SCREEN_WIDTH, CELL_SIZE):  # 绘制垂直网格线
            self.draw.line(self.background, GRID_COLOR, (_, 0), (_, SCREEN_HEIGHT))
        for _ in range(CELL_SIZE, SCREEN_HEIGHT, CELL_SIZE):  # 绘制水平网格线
            self.draw.line(self.background, GRID_COLOR, (0, _), (SCREEN_WIDTH, _))

    def restart(self):
        """重启游戏"""
        if not self.snake.is_alive:  # 如果蛇已经死亡
            self.apple_count = 0  # 重置苹果计数器
            self.apple.drop()  # 重新放置苹果
            self.snake.restart_pawn()  # 重生蛇
            self.running = True  # 继续游戏循环

    def draw_score(self):
        """绘制分数"""
        text = f"Apple: {self.apple_count}"  # 准备要绘制的文本
        self.high_score = max(self.high_score, self.apple_count)  # 更新最高分
        self.draw_text(text, (0, 0), (255, 255, 33))  # 绘制文本

        if not self.snake.is_alive:  # 如果蛇已经死亡
            self.draw_text(" 游戏结束 ", (SCREEN_WIDTH / 2 - 54, SCREEN_HEIGHT / 2 - 10),  # 绘制游戏结束文本
                           (255, 33, 33), WHITE)

            self.draw_text(" 按R键重启 ", (SCREEN_WIDTH / 2 - 85, SCREEN_HEIGHT / 2 + 20),  # 绘制重启提示文本
                           GREY, DARK_GREY)

            self.draw_text(f"当前最高分: {self.high_score}", (SCREEN_WIDTH / 2 - 114, SCREEN_HEIGHT / 2 + 50),  # 绘制最高分文本
                           (255, 33, 33), WHITE)  # 展示最高分

        if not self.running and self.snake.is_alive:  # 如果游戏暂停且蛇还活着
            self.draw_text("游戏暂停 ", (SCREEN_WIDTH / 2 - 55, SCREEN_HEIGHT / 2 - 10),  # 绘制游戏暂停文本
                           LIGHT_GREY, DARK_GREY)


if __name__ == '__main__':
    SnakeGame().run()  # 运行游戏
