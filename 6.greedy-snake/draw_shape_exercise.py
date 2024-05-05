# -*- encoding:utf-8 -*-
# @日期和时间：2023/10/13 10:09
# @Author: Kenny cai
# @File name:draw_shape_exercise.py
# @dev tool:PyCharm

import pygame

def main():
    pygame.init()
    window = pygame.display.set_mode((600, 600))
    color = (0, 0, 255)
    rect = pygame.Rect(10, 10, 20, 20)
    pt1 = (10, 100)
    pt2 = (200, 20)
    pt3 = (100, 200)
    points = [pt1, pt2, pt3]
    points2 = [pt1, pt2, (250,100),pt3]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        # pygame.draw.rect(window, color, rect)
        # pygame.draw.rect(window, color, rect,2) # 指定第四个参数并且设置为2指的是线宽为2.绘制空心图形
        # pygame.draw.ellipse(window, color, rect) # 绘制圆也需要矩形作为基础
        # pygame.draw.circle(window,color,(100,100),20) # 绘制圆的方法二比较麻烦没有ellipse方法好
        # pygame.draw.ellipse(window, color, rect,2)
        # pygame.draw.line(window, color, pt1,pt2,3)
        # pygame.draw.lines(window, color, False,points,3) # 第三个参数为False，只绘制两条直线
        # pygame.draw.lines(window, color,True, points,3) # 第三个参数为True，绘制三角形
        # pygame.draw.polygon(window,color,points) # 绘制实心多边形，会根据顶点的个数来绘制几边形
        pygame.draw.polygon(window,color,points2) # 绘制实心多边形，会根据顶点的个数来绘制几边形
        # pygame.draw.arc(window,color,rect,6.28,9) # 绘制圆弧，也是需要rect对象
        pygame.display.update()

if __name__ == '__main__':
    main()