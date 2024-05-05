# -*- encoding:utf-8 -*-
# @日期和时间：2023/10/6 11:08
# @Author: Kenny cai
# @File name:main.py.py
# @dev tool:PyCharm


"""
跟着麦叔学习开发飞机打敌人游戏
"""
import pygame
import random
import math

# 初始化游戏组件
pygame.init()
# 设置显示窗口
screen = pygame.display.set_mode((800, 600))
# 设置窗口标题
pygame.display.set_caption('飞机打外星人游戏')
# 加载游戏图标
icon = pygame.image.load('ufo.png')
# 设置游戏图标
pygame.display.set_icon(icon)

#  加载背景图片，此时在内存里，面需要在游戏循环里面绘制
bg = pygame.image.load('bg.png')
# 添加背景音效
# pygame.mixer.music.load('house_lo.wav')
pygame.mixer.music.load('bg.wav')
pygame.mixer.music.play(-1)  # 参数-1表示一直播放
# 添加击中音效
exp_sound = pygame.mixer.Sound('exp.wav')

#  加载飞机
player = pygame.image.load('player.png')  # 飞机图片的大小是64 X 64
#  定义两个变量保存飞机的坐标方便移动飞机的代码修改
playerX, playerY = 400, 500
# 飞机移动方向控制正数往右移动，负数往左移动，大小是移动的速度
playerStep = 0

# 分数
score = 0
# 创建一个字体用于显示分数
font = pygame.font.Font('./汉仪大黑简.ttf', 32)


# 定义一个显示分数的函数
def show_score():
    # 拼接显示文本
    text = f'分数：{score}'
    score_render = font.render(text, True, (255, 255, 255))
    screen.blit(score_render, (10, 10))


#  设置一个游戏结束标记,默认是False
is_over = False

#  添加敌人，往往有多个
number_of_enemy = 6  # 指定敌人的数量


# 定义一个敌人类，方便管理
class Enemy:
    def __init__(self):
        self.img = pygame.image.load('enemy.png')
        self.x = random.randint(200, 600)
        self.y = random.randint(50, 250)
        self.step = random.randint(2, 6)

    # 给敌人类添加一个重新设置坐标
    def reset(self):
        self.x = random.randint(200, 600)
        self.y = random.randint(50, 200)


# 定义一个子弹类
class Bullet:
    def __init__(self):
        self.img = pygame.image.load('bullet.png')
        self.x = playerX + 16
        self.y = playerY + 10
        self.step = 10

    # 击中检测
    def hit(self):
        """

        :return:
        """
        global score
        # 需要遍历使用敌人
        for e in enemies:
            # 如果距离小于我们设置的值，我们就认为它被击中
            if (distance(self.x, self.y, e.x, e.y) < 30):
                # 击中处理
                exp_sound.play()
                # 1 加分
                score += 1
                # print("score: ",score)
                show_score()
                # 2 从容器不是空的从容器里面移除一颗子弹
                if len(bullets) > 0:
                    bullets.remove(self)
                    e.reset()  # 被击中了敌人会重新设置坐标？！！相当于被击中的就消失了，然后在另外一个地方产生一个新敌人
                else:
                    break


# 创建敌人
enemies = []
for i in range(number_of_enemy):
    enemies.append(Enemy())


# 定义一个显示敌人的方法
def show_enemy():
    global is_over
    """
    移动敌人的函数
    :return: 
    """
    for e in enemies:
        screen.blit(e.img, (e.x, e.y))
        e.x += e.step
        # 出界处理,达到出界的位置就改变方向并且往下沉一下
        if e.x > screen.get_width() - 64 or e.x < 0:
            e.step *= -1
            e.y += 20
            # 判断游戏结束的条件：当敌人低于飞机的高度就结束
            if e.y > 450:
                is_over = True
                enemies.clear()


def check_game_state():
    global is_over
    if is_over:
        game_over()


def game_over():
    font2 = pygame.font.Font('./汉仪大黑简.ttf', 64)
    text = 'Game Over'
    render = font2.render(text, True, (255, 255, 255))
    screen.blit(render, (250, 250))


bullets = []  # 保存子弹的容器，需要注意：只要子弹出界了，我们就把它从容器中移除


def show_bullets():
    """
    显示子弹并且改变位置
    :return:
    """
    for b in bullets:
        screen.blit(b.img, (b.x, b.y))
        b.hit()  # 射击检测，在这里比较好
        b.y -= b.step
        # 如果出界就把它从容器里面移除
        if b.y < 0:
            if len(bullets) > 0:
                bullets.remove(b)


# 计算两点之间距离
def distance(bx, by, ex, ey):
    return math.sqrt((ex - bx) ** 2 + (ey - by) ** 2)


# print(distance(1, 1, 4, 5))
#  设置游戏标记
running = True


def process_events():
    """
    把主要的事件处理逻辑封装为一个函数，这样子可以使得代码层次比较清晰
    :return:  None
    """
    global running, playerStep
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # 注册键盘事件处理,如果是键盘的键被按下了,就需要动
        if event.type == pygame.KEYDOWN:
            # print('key down....')
            if event.key == pygame.K_LEFT:
                # print('left...')
                playerStep = -2
            elif event.key == pygame.K_RIGHT:
                playerStep = 2
            # 添加对空格键按下的相应，是可以用来创建并且发射子弹的
            elif event.key == pygame.K_SPACE:
                # print('space pressed...')
                b = Bullet()
                bullets.append(b)
                print("len:", len(bullets))

        # 如果键盘的键弹起，就不要动
        if event.type == pygame.KEYUP:
            playerStep = 0


def move_player():
    """
    玩家移动出界处理
    :return:
    """
    global playerX
    # 出界处理
    width_limit = screen.get_width() - 64
    if playerX >= width_limit:
        playerX = width_limit
    if playerX < 0:
        playerX = 0


# 游戏主循环

while running:
    # 设置背景,用我们生成的screen对象的blit方法绘制背景，需要调用pygame.display.update()方法更新显示
    screen.blit(bg, (0, 0))
    # if is_over:
    #     game_over()
    show_score()
    #  事件处理
    process_events()
    screen.blit(player, (playerX, playerY))
    playerX += playerStep  # 向右移动
    move_player()
    show_enemy()
    show_bullets()
    check_game_state()
    pygame.display.update()  # 和界面显示有关的代码必须放在这一句的前面，否则没有效果
