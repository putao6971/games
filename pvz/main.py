import os
import time
import pygame
from pvz.plant.Peashooter import Peashooter
from pvz.plant.SunFlower import SunFlower
from pvz.plant.WallNut import WallNut
from pvz.plant.Sun import Sun
from pvz.plant.Sun2 import Sun2
from pvz.plant.JXC import JXC
from pvz.plant.Bullet import Bullet
from pvz.plant.BulletJXC import BulletJXC
from pvz.zombie.Zombie import Zombie
from pvz.zombie.ZombieLz import ZombieLz

# 初始化pygame库
pygame.init()

# 设置游戏背景尺寸，所有的资源图片都是基于这个尺寸制作的，不建议修改
background_size = (820, 560)

# 创建游戏窗口并设置标题
screen = pygame.display.set_mode(background_size)
pygame.display.set_caption("植物大战僵尸 By stormsha")

# 获取当前工作目录
base_path = os.getcwd()

# 加载背景图片
bg_img_obj = pygame.image.load(os.path.join(base_path, 'images/a3.png')).convert_alpha()

# 加载植物图片
sunFlowerImg = pygame.image.load(os.path.join(base_path, 'images/SunFlower/SunFlower_00.png')).convert_alpha()
wallNutImg = pygame.image.load(os.path.join(base_path, 'images/WallNut/wall_nut_00.png')).convert_alpha()
peaShooterImg = pygame.image.load(os.path.join(base_path, 'images/Peashooter/Peashooter00.png')).convert_alpha()
jxcImg = pygame.image.load(os.path.join(base_path, 'images/jxc/JXC00.png')).convert_alpha()

# 加载阳光储蓄罐和种子图片
sun_back_img = pygame.image.load(os.path.join(base_path, 'images/SeedBank01.png')).convert_alpha()
sunflower_seed = pygame.image.load(os.path.join(base_path, 'images/SunFlower_kp.png'))
wall_nut_seed = pygame.image.load(os.path.join(base_path, 'images/Wallnut_kp.png'))
peashooter_seed = pygame.image.load(os.path.join(base_path, 'images/Peashooter_kp.png'))
jxc_seed = pygame.image.load(os.path.join(base_path, 'images/jxc_kp.png'))

# 初始化阳光值为100
text = "1000"

# 设置阳光值字体和颜色
sun_font = pygame.font.SysFont("黑体", 25)
sun_num_surface = sun_font.render(str(text), True, (0, 0, 0))

# 创建植物组、子弹组、僵尸组和阳光组
spriteGroup = pygame.sprite.Group()
bulletGroup = pygame.sprite.Group()
zombieGroup = pygame.sprite.Group()
sun_sprite = pygame.sprite.Group()

# 定义游戏时钟和特殊事件
clock = pygame.time.Clock()
GEN_SUN_EVENT = pygame.USEREVENT + 1  # 生成阳光事件
pygame.time.set_timer(GEN_SUN_EVENT, 2000)  # 每2秒生成一次阳光
GEN_BULLET_EVENT = pygame.USEREVENT + 2  # 生成子弹事件
pygame.time.set_timer(GEN_BULLET_EVENT, 2000)  # 每2秒生成一次子弹
GEN_ZOMBIE_EVENT = pygame.USEREVENT + 3  # 生成僵尸事件
pygame.time.set_timer(GEN_ZOMBIE_EVENT, 10000)  # 每10秒生成一次僵尸
GEN_SUN2_EVENT = pygame.USEREVENT + 4  # 生成双倍阳光事件
pygame.time.set_timer(GEN_SUN2_EVENT, 20000)  # 每20秒生成一次双倍阳光

# 初始化选择的植物类型和僵尸数量
choose = 0
zombie_num = 0


def main():
    """
    游戏主函数，包含游戏主循环
    """
    global zombie_num  # 僵尸数量全局变量
    global choose  # 选择的植物类型全局变量
    global text  # 阳光值全局变量
    global sun_num_surface  # 阳光值显示表面全局变量
    running = True  # 游戏是否运行标志
    index = 0  # 用于植物、子弹和僵尸的更新和绘制的索引

    while running:
        # 控制游戏帧率
        clock.tick(20)

        # 检查子弹和僵尸的碰撞，如果碰撞则减少僵尸的能量并移除子弹
        for bullet in bulletGroup:
            for zombie in zombieGroup:
                if pygame.sprite.collide_mask(bullet, zombie):
                    if isinstance(bullet, BulletJXC):  # 如果是坚果的子弹，则减少2点能量
                        zombie.energy -= 2
                        bulletGroup.remove(bullet)
                    else:  # 否则减少1点能量
                        zombie.energy -= 1
                        bulletGroup.remove(bullet)

        # 检查植物和僵尸的碰撞，如果碰撞则设置僵尸的GO标志为True，并将僵尸添加到植物的zombies列表中
        for sprite in spriteGroup:
            for zombie in zombieGroup:
                if pygame.sprite.collide_mask(sprite, zombie):
                    zombie.GO = True
                    sprite.zombies.add(zombie)
                # 如果植物是坚果，则检查僵尸是否在攻击范围内，如果是则设置植物的攻击标志为True，并生成子弹
                if isinstance(sprite, JXC):
                    if abs(zombie.rect.top - sprite.rect[1]) <= 40 and zombie.rect.left < 760:
                        sprite.attack = True
                        if sprite.att == 11:
                            bullet_jxc = BulletJXC(sprite.rect, background_size, zombie.rect[0])
                            bulletGroup.add(bullet_jxc)
                            break

        # 在屏幕上绘制背景、阳光储蓄罐、阳光值和种子图片
        screen.blit(bg_img_obj, (0, 0))
        screen.blit(sun_back_img, (20, 0.5))
        screen.blit(sun_num_surface, (35, 50))
        screen.blit(sunflower_seed, (80, 5))
        screen.blit(peashooter_seed, (121, 5))
        screen.blit(wall_nut_seed, (162, 5))
        screen.blit(jxc_seed, (203, 5))

        # 更新和绘制植物、子弹、僵尸和阳光
        spriteGroup.update(index)
        spriteGroup.draw(screen)
        bulletGroup.update(index)
        bulletGroup.draw(screen)
        zombieGroup.update(index)
        zombieGroup.draw(screen)
        sun_sprite.update(index)
        sun_sprite.draw(screen)

        # 获取鼠标位置，并在鼠标位置上绘制选择的植物预览图
        (x, y) = pygame.mouse.get_pos()
        if choose == 1:
            screen.blit(sunFlowerImg, (x - sunFlowerImg.get_rect().width // 2, y - sunFlowerImg.get_rect().height // 2))
        if choose == 2:
            screen.blit(peaShooterImg,
                        (x - peaShooterImg.get_rect().width // 2, y - peaShooterImg.get_rect().height // 2))
        if choose == 3:
            screen.blit(wallNutImg, (x - wallNutImg.get_rect().width // 2, y - wallNutImg.get_rect().height // 2))
        if choose == 4:
            screen.blit(jxcImg, (x - jxcImg.get_rect().width // 2, y - jxcImg.get_rect().height // 2))

        # 增加索引值
        index += 1

        # 处理pygame事件
        for event in pygame.event.get():
            # 处理生成双倍阳光事件
            if event.type == GEN_SUN2_EVENT:
                sun2 = Sun2()
                sun_sprite.add(sun2)
            # 处理生成僵尸事件
            if event.type == GEN_ZOMBIE_EVENT:
                zombie_num += 1
                zombie = Zombie()
                zombie_lz = ZombieLz()
                if 0 < zombie_num <= 15:
                    zombieGroup.add(zombie)
                if zombie_num > 7:
                    zombieGroup.add(zombie_lz)
            # 处理生成阳光事件
            if event.type == GEN_SUN_EVENT:
                for sprite in spriteGroup:
                    if isinstance(sprite, SunFlower):
                        now = time.time()
                        if now - sprite.last_time >= 10:  # 如果距离上次生成阳光的时间大于等于10秒，则生成阳光
                            sun = Sun(sprite.rect)
                            sun_sprite.add(sun)
                            sprite.last_time = now
            # 处理生成子弹事件
            if event.type == GEN_BULLET_EVENT:
                for sprite in spriteGroup:
                    for zombie in zombieGroup:
                        if isinstance(sprite, Peashooter) \
                                and 0 < sprite.rect[1] - zombie.rect[1] < 50 \
                                and zombie.rect[0] < 760:
                            bullet = Bullet(sprite.rect, background_size)
                            bulletGroup.add(bullet)
                            break
            # 处理退出游戏事件
            if event.type == pygame.QUIT:
                running = False
            # 处理鼠标点击事件
            if event.type == pygame.MOUSEBUTTONDOWN:
                pressed_key = pygame.mouse.get_pressed()
                if pressed_key[0]:
                    pos = pygame.mouse.get_pos()
                    x, y = pos
                    # 如果点击了种子按钮，则设置选择的植物类型
                    if 80 <= x < 121 and 5 <= y <= 63 and int(text) >= 50:
                        choose = 1
                    elif 121 <= x < 162 and 5 <= y <= 63 and int(text) >= 100:
                        choose = 2
                    elif 162 <= x < 203 and 5 <= y <= 63 and int(text) >= 50:
                        choose = 3
                    elif 203 <= x < 244 and 5 <= y <= 63 and int(text) >= 100:
                        choose = 4
                    # 如果点击了游戏区域，则根据选择的植物类型放置植物
                    elif 36 < x < 800 and 70 < y < 550:
                        if choose == 1:
                            true_x = x // 90 * 85 + 35  # 计算植物的左上角坐标
                            true_y = y // 100 * 95 - 15
                            can_hold = True  # 是否可以放置植物标志
                            for sprite in spriteGroup:
                                if sprite.rect.left == true_x and sprite.rect.top == true_y:
                                    can_hold = False
                                    break
                            if not can_hold or true_y < 25:
                                break
                            sunflower = SunFlower(time.time(), (true_x, true_y))  # 创建向日葵实例
                            spriteGroup.add(sunflower)  # 将向日葵添加到植物组中
                            choose = 0  # 重置选择的植物类型
                            text = int(text)  # 将阳光值转换为整数
                            text -= 50  # 减少50阳光
                            my_font = pygame.font.SysFont("黑体", 25)  # 设置字体
                            sun_num_surface = my_font.render(str(text), True, (0, 0, 0))  # 更新阳光值显示表面
                        if choose == 2:
                            true_x = x // 90 * 85 + 32
                            true_y = y // 100 * 95 - 18
                            can_hold = True
                            for sprite in spriteGroup:
                                if sprite.rect.left == true_x and sprite.rect.top == true_y:
                                    can_hold = False
                                    break
                            if not can_hold or true_y < 25:
                                break
                            peashooter = Peashooter((true_x, true_y))  # 创建豌豆射手实例
                            spriteGroup.add(peashooter)  # 将豌豆射手添加到植物组中
                            choose = 0
                            text = int(text)
                            text -= 100  # 减少100阳光
                            my_font = pygame.font.SysFont("黑体", 25)
                            sun_num_surface = my_font.render(str(text), True, (0, 0, 0))
                        if choose == 3:
                            true_x = x // 90 * 85 + 35
                            true_y = y // 100 * 95 - 15
                            can_hold = True
                            for sprite in spriteGroup:
                                if sprite.rect.left == true_x and sprite.rect.top == true_y:
                                    can_hold = False
                                    break
                            if not can_hold or true_y < 25:
                                break
                            wall_nut = WallNut((true_x, true_y))  # 创建坚果实例
                            spriteGroup.add(wall_nut)  # 将坚果添加到植物组中
                            choose = 0
                            text = int(text)
                            text -= 50  # 减少50阳光
                            my_font = pygame.font.SysFont("黑体", 25)
                            sun_num_surface = my_font.render(str(text), True, (0, 0, 0))
                        if choose == 4:
                            true_x = x // 90 * 85 + 22
                            true_y = y // 100 * 95 - 35
                            can_hold = True
                            for sprite in spriteGroup:
                                if sprite.rect.left == true_x and sprite.rect.top == true_y:
                                    can_hold = False
                                    break
                            if not can_hold or true_y < 25:
                                break
                            jxc = JXC((true_x, true_y))  # 创建坚果墙实例
                            spriteGroup.add(jxc)  # 将坚果墙添加到植物组中
                            choose = 0
                            text = int(text)
                            text -= 100  # 减少100阳光
                            my_font = pygame.font.SysFont("黑体", 25)
                            sun_num_surface = my_font.render(str(text), True, (0, 0, 0))
                    # 如果点击了阳光，则收集阳光并更新阳光值显示表面
                    for sun in sun_sprite:
                        if sun.rect.collidepoint(pos):
                            sun_sprite.remove(sun)
                            text = str(int(text) + 25)
                            sun_font = pygame.font.SysFont("黑体", 25)
                            sun_num_surface = sun_font.render(str(text), True, (0, 0, 0))
            # 检查僵尸是否到达终点或游戏是否胜利
            for zombie in zombieGroup:
                if zombie.rect.left == -120:  # 如果僵尸到达终点，则游戏失败
                    print("你的脑子被僵尸吃了")
                    running = False
                if zombie_num > 20:  # 如果僵尸数量大于20，则游戏胜利
                    print("胜利")
                    running = False

        # 更新游戏界面
        pygame.display.update()


if __name__ == '__main__':
    main()