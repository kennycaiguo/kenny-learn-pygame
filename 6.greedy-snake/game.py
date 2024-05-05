# -*- encoding:utf-8 -*-
# @日期和时间：2023/10/8 16:07
# @Author: Kenny cai
# @File name:game.py
# @dev tool:PyCharm

"""
pygame 开发贪吃蛇小游戏，这个是主游戏程序
"""
import pygame
import sys
from game_item import *  # 导入其他类


class Game:
    def __init__(self):
        self.main_window = pygame.display.set_mode((640, 480))
        pygame.display.set_caption('Python贪吃蛇游戏')  # 设置窗口标题
        self.score_label = Label()
        #  分数文本标签
        # self.score = 0
        #  游戏暂停/结束提示文本标签
        self.tip_label = Label(24, False)
        #  游戏结束标记
        self.is_game_over = False
        # self.is_game_over = True
        #  游戏暂停标记
        self.is_pause = False
        # 添加食物属性
        self.food = Food()
        # 添加蛇
        self.snake = Snake()

    def start(self):  # 启动游戏

        # 创建游戏时钟对象，用来控制游戏循环的频率
        clock = pygame.time.Clock()
        # 实例化应该食物

        while True:
            # 事件处理,判断是否是退出，如果是，就退出
            for event in pygame.event.get():
                # 检测用户是否点击了窗口上面的x
                if event.type == pygame.QUIT:
                    return False
                # 检测键盘esc按下
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # 按下esc键也会退出程序
                        return False
                    # 空格键按下检测
                    elif event.key == pygame.K_SPACE:
                        # 先判断游戏是否以及结束了，如果是，就启动游戏
                        if self.is_game_over:
                            self.reset_game()
                        # 如果没有暂停就暂停
                        else:
                            self.is_pause = not self.is_pause

                    # 需要确定在没有暂停或者游戏结束，才需要监听食物更新事件
                if not self.is_pause and not self.is_game_over:
                    # 监听自定义的FOOD_UPDATE_EVEN事件
                    if event.type == FOOD_UPDATE_EVENT:
                        # 30秒食物没有被吃掉就要更新他的位置
                        self.food.random_rect()
                    # 监听蛇更新事件
                    elif event.type == SNAKE_UPDATE_EVENT:
                        # 移动蛇身体
                        self.is_game_over = not self.snake.update()
                    elif event.type == pygame.KEYDOWN:
                        # 监听上下左右方向键的按下事件并且调用蛇的改变方向方法
                        # 写法1
                        # if event.key == pygame.K_RIGHT:
                        #     self.snake.change_dir(pygame.K_RIGHT)
                        # elif event.key == pygame.K_LEFT:
                        #     self.snake.change_dir(pygame.K_LEFT)
                        # elif event.key == pygame.K_UP:
                        #     self.snake.change_dir(pygame.K_UP)
                        # elif event.key == pygame.K_DOWN:
                        #     self.snake.change_dir(pygame.K_DOWN)
                        # 写法2
                        if event.key in (pygame.K_RIGHT,pygame.K_LEFT,pygame.K_UP,pygame.K_DOWN):
                            self.snake.change_dir(event.key)




            # 依次绘制游戏元素
            self.main_window.fill(BACKGROUND_COLOR)  # 设置背景颜色

            self.score_label.draw(self.main_window, f"得分：{self.snake.score}")  # 这一句必须要在食物绘制之前执行

            # 当游戏已经结束，显示重新开始提示文本
            if self.is_game_over:
                self.tip_label.draw(self.main_window, "游戏已经结束，按空格键开始新游戏")
            #  当暂停标记为True，需要显示暂停文本
            elif self.is_pause:
                self.tip_label.draw(self.main_window, f"游戏已经暂停，按空格键继续")
            else:
                # 判断是否吃到食物
                if self.snake.has_eat(self.food):
                    self.food.random_rect()


            #绘制食物
            self.food.draw(self.main_window)
            # 绘制蛇
            self.snake.draw(self.main_window)
            # # 吃食物
            # if self.snake.has_eat(self.food):
            #     self.food.random_rect()



            pygame.display.update()
            clock.tick(60)

    def reset_game(self):
        """
        游戏重置功能
        :return:
        """
        # self.score = 0
        #  游戏结束标记
        self.is_game_over = False
        #  游戏暂停标记
        self.is_pause = False
        # 重置蛇的数据
        self.snake.reset_snake()
        # 重新绘制食物
        self.food.random_rect()


def main():
    # 1.初始化
    pygame.init()
    # 2.创建主窗口,需要创建一个Game类然后调用它的__init__方法
    Game().start()

    pygame.quit()  # 释放游戏资源


if __name__ == '__main__':
    main()
