# -*- encoding:utf-8 -*-
# @日期和时间：2023/10/9 9:36
# @Author: Kenny cai
# @File name:game_item.py
# @dev tool:PyCharm

"""
游戏相关的对象，封装蛇，标签，食物等类和所有游戏的全局变量都在这里定义，在别的模块里面需要使用from game_item import *
"""

import pygame
import random

#  全局变量
BACKGROUND_COLOR = (232, 232, 232)
SCORE_TEXT_COLOR = (192, 192, 192)  # 分数文本的颜色
TIP_TEXT_COLOR = (64, 64, 64)  # 提示文本的颜色
# 需要获取游戏主窗口的大小，然后把它等分为一个个的小格子方便绘制蛇
SCREEN_RECT = pygame.Rect(0, 0, 640, 480)
CELL_SIZE = 20  # 每一个小格子的大小
#  定义定时器常量标志：更新食物事件
FOOD_UPDATE_EVENT = pygame.USEREVENT
SNAKE_UPDATE_EVENT = pygame.USEREVENT + 1


#  Label类
class Label(object):
    """
    文本标签类
    """

    def __init__(self, size=48, is_score=True):
        """
        初始化方法
        """
        self.font = pygame.font.SysFont('simhei', size)
        self.is_score = is_score

    def draw(self, window, text):
        """
        绘制当前对象的内容
        :return:
        """
        # 渲染文字，生成一个文字相关的图像
        color = SCORE_TEXT_COLOR if self.is_score else TIP_TEXT_COLOR  # python仿三元运算符
        text_surface = self.font.render(text, True, color)
        # 获取文本的外接矩形
        text_rect = text_surface.get_rect()
        # 获取窗口的矩形
        window_rect = window.get_rect()
        # 设置显示位置,需要判断如果是分数就显示在窗口左下角如果是提示信息，显示在屏幕中央
        if self.is_score:
            text_rect.bottomleft = window_rect.bottomleft
        else:
            text_rect.center = window_rect.center

        # 显示字体图像
        window.blit(text_surface, text_rect)


#  食物类
class Food(object):
    def __init__(self):
        self.color = (255, 0, 0)  # 食物的颜色设置为红色
        self.score = 10  # 每吃掉一个食物得10分
        self.rect = pygame.Rect(0, 0, CELL_SIZE, CELL_SIZE)  # 食物位置，
        self.random_rect()  # 随机生成的食物的位置

    # 绘制食物的方法
    def draw(self, window):
        # 先判断食物的矩形区域是否达到格子的大小
        if self.rect.w < CELL_SIZE:
            self.rect.inflate_ip(2, 2)  # 每一次增加2像素
        pygame.draw.ellipse(window, self.color, self.rect)

    # 随机生成食物的位置的方法
    def random_rect(self):
        # 根据游戏主窗口的大小和单元格的大小计算行数和列数
        cols= SCREEN_RECT.w / CELL_SIZE - 1
        rows= SCREEN_RECT.h / CELL_SIZE - 1

        x = random.randint(0, cols) * CELL_SIZE
        y = random.randint(0, rows) * CELL_SIZE

        self.rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        # 把矩形设置为不可见方便在绘制的时候做动画效果
        self.rect.inflate_ip(-CELL_SIZE, -CELL_SIZE)  # 这个方法修改原来的矩形，它没有返回值
        # 定时器事件，每30秒触发一次食物更新事件
        pygame.time.set_timer(FOOD_UPDATE_EVENT, 30000)


#
# 蛇类
class Snake(object):
    """
    蛇类
    """

    def __init__(self):
        self.dir = pygame.K_RIGHT  # 默认蛇是向右移动的
        self.time_interval = 500
        self.score = 0
        self.color = (64, 64, 64)
        self.body_list = []
        self.reset_snake()

    def reset_snake(self):
        self.dir = pygame.K_RIGHT
        self.time_interval = 500
        self.score = 0
        self.body_list.clear()
        for _ in range(3):
            self.add_node()

    def add_node(self):
        # 如果蛇不是空的，就把头部矩形复制一份
        # head = None
        if self.body_list:
            head = self.body_list[0].copy()
        else:
            # 如果是空的，就生成一个节点,注意在窗口外面
            head = pygame.Rect(-CELL_SIZE, 0, CELL_SIZE, CELL_SIZE)
        # 需要根据移动方向把新生成的头部放到适合的位置
        if self.dir == pygame.K_RIGHT:
            head.x += CELL_SIZE
        elif self.dir == pygame.K_LEFT:
            head.x -= CELL_SIZE
        elif self.dir == pygame.K_UP:
            head.y -= CELL_SIZE
        elif self.dir == pygame.K_DOWN:
            head.y += CELL_SIZE
        # 把头添加到身体列表的前面
        self.body_list.insert(0, head)
        # 定时更新身体
        pygame.time.set_timer(SNAKE_UPDATE_EVENT, self.time_interval)

    def draw(self, window):
        # 需要遍历body_list来绘制每一个节点
        for idx, rect in enumerate(self.body_list):
            pygame.draw.rect(window, self.color, rect.inflate(-2, -2), idx == 0)  # idx == 0 表示作为头部的矩形不填充颜色

    def update(self):
        # 移动前记录身体状态并且备份身体列表
        body_list_copy = self.body_list.copy()
        # 移动身体添加一个头，删除一个尾
        self.add_node()
        self.body_list.pop()
        # 判断蛇死亡后的处理,还原死前的身体列表
        if self.is_dead():
            self.body_list = body_list_copy
            return False
        return True

    def change_dir(self, to_dir):
        hor_dirs = (pygame.K_LEFT, pygame.K_RIGHT)
        ver_dirs = (pygame.K_UP, pygame.K_DOWN)
        if (self.dir in hor_dirs and to_dir not in hor_dirs) or (self.dir in ver_dirs and to_dir not in ver_dirs):
            self.dir = to_dir

    def has_eat(self, food):
        # 判断蛇头于食物是否重叠 #如果是，就把蛇的分数加10
        if self.body_list[0].contains(food.rect):
            # 蛇加分
            self.score += food.score
            # 加快蛇移动速度
            if self.time_interval > 100:
                self.time_interval -= 50
            # 蛇身体增加一节
            self.add_node()
            # 返回True表示吃到食物
            return True
        return False  # 返回False表示没有吃到食物

    # 添加判断蛇是否死亡的方法
    def is_dead(self):
        # 获取蛇头的矩形
        head = self.body_list[0]
        # 判断蛇头是否不在窗体里
        if not SCREEN_RECT.contains(head):
            return True
        # 判断蛇头是否与身体重叠
        for rect in self.body_list[1:]:
            if head.contains(rect):
                return True
        return False
