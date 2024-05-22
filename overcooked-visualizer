"""介绍：
使用pygame进行可视化速度和移动方向
管道存放在./QtOvercooked/pipe/visualize
log文件存放在./QtOvercooked/pipe/log.txt

# 输入内容：
p1x,p1y 角色1的位置
v1x,v1y 角色1的移动xy速度
a1x,a1y 角色1的移动方向 只能是-1,0,1
p2x,p2y 角色2的位置
v2x,v2y 角色2的移动xy速度
a2x,a2y 角色2的移动方向 只能是-1,0,1

# 输入格式：
一行，每个数据之间用空格隔开

# 使用方法：
python3 visualize.py进行管道模式
python3 visualize.py 1进行log模式
按左右键可以快进快退，按上下键可以调整帧率

# 要求：
管道模式下,先运行该文件,再运行QtOvercooked,在QtOvercooked中每一帧按照上述格式写入管道
log模式下,先运行QtOvercooked,在QtOvercooked中每一帧按照上述格式写入一行到log.txt

"""

import pygame
import sys
import os
import time


def draw(speed, frame, data: list):
    [p1x, p1y, v1x, v1y, a1x, a1y, p2x, p2y, v2x, v2y, a2x, a2y] = [
        float(i) for i in data
    ]
    position1 = (
        p1x * width / maxwidth + margin / 2,
        p1y * height / maxheight + margin / 2,
    )
    speed1 = (v1x * maxlength / maxspeed, v1y * maxlength / maxspeed)
    move1 = (a1x * maxlength / maxmove, a1y * maxlength / maxmove)
    position2 = (
        p2x * width / maxwidth + margin / 2,
        p2y * height / maxheight + margin / 2,
    )
    speed2 = (v2x * maxlength / maxspeed, v2y * maxlength / maxspeed)
    move2 = (a2x * maxlength / maxmove, a2y * maxlength / maxmove)
    # 绘图
    screen.fill((255, 255, 255))
    dark_blue = (0, 0, 128)
    dark_green = (0, 128, 0)
    dark_red = (128, 0, 0)
    shadow1 = (255, 200, 200)  # light red
    shadow2 = (200, 255, 200)  # light green
    # 绘制格子
    for i in range(1, maxwidth):
        pygame.draw.line(
            screen,
            dark_blue,
            (i * width / maxwidth + margin / 2, margin / 2),
            (i * width / maxwidth + margin / 2, height + margin / 2),
            1,
        )
    for i in range(1, maxheight):
        pygame.draw.line(
            screen,
            dark_blue,
            (margin / 2, i * height / maxheight + margin / 2),
            (width + margin / 2, i * height / maxheight + margin / 2),
            1,
        )
    # 绘制角色位置
    pygame.draw.circle(screen, shadow1, position1, 35)
    pygame.draw.circle(screen, shadow2, position2, 35)
    # 在角色周围绘制移动
    pygame.draw.circle(
        screen,
        dark_red,
        (move1[0] + position1[0], move1[1] + position1[1]),
        15,
    )
    pygame.draw.circle(
        screen,
        dark_green,
        (move2[0] + position2[0], move2[1] + position2[1]),
        15,
    )
    # 在角色周围绘制速度
    pygame.draw.line(
        screen,
        dark_blue,
        position1,
        (speed1[0] + position1[0], speed1[1] + position1[1]),
        10,
    )
    pygame.draw.line(
        screen,
        dark_blue,
        position2,
        (speed2[0] + position2[0], speed2[1] + position2[1]),
        10,
    )
    # 在左上角显示帧数和帧率
    font = pygame.font.Font(None, 36)
    text = font.render(
        "Frame: " + str(frame) + ", Speed: " + str(speed), 1, (10, 10, 10)
    )
    screen.blit(text, (10, height + margindown - 30))
    # 显示数据
    font = pygame.font.Font(None, 36)
    text = font.render(
        f"({str(p1x)[:4]},{str(p1y)[:4]}) ({str(v1x)[:4]},{str(v1y)[:4]}) ({str(a1x)[:4]},{str(a1y)[:4]}) red",
        1,
        (10, 10, 10),
    )
    screen.blit(text, (10, height + margindown + 10))
    text = font.render(
        f"({str(p2x)[:4]},{str(p2y)[:4]}) ({str(v2x)[:4]},{str(v2y)[:4]}) ({str(a2x)[:4]},{str(a2y)[:4]}) green",
        1,
        (10, 10, 10),
    )
    screen.blit(text, (10, height + margindown + 50))
    pygame.display.update()


def create_pipe(pipe_path):
    # 新建管道
    if not os.path.exists(pipe_path):
        os.mkfifo(pipe_path)


def init_draw(size):
    # 初始化pygame
    pygame.init()
    # 设置窗口
    global screen
    screen = pygame.display.set_mode(size)
    # 设置窗口标题
    pygame.display.set_caption("Visualize")


if __name__ == "__main__":
    pipe_mode = True
    if len(sys.argv) == 2:
        pipe_mode = False
    # 管道路径
    pipe_path = "./QtOvercooked/pipe/visualize"
    if pipe_mode:
        # 先删除管道
        if os.path.exists(pipe_path):
            os.remove(pipe_path)
        # 创建管道
        create_pipe(pipe_path)
    else:
        with open("./QtOvercooked/pipe/log.txt", "r") as f:
            whole_data = f.readlines()

    # 设置窗口大小
    width, height = 800, 800
    margin = 100
    margindown = 100
    center = width // 2, height // 2
    maxlength = 50
    maxheight = 10
    maxwidth = 10
    maxspeed = 5
    maxmove = 1
    size = width + margin, height + margin + margindown
    # 初始化
    init_draw(size)

    # 获取当前时间
    last_time = time.time()
    done = False
    frame = 0
    frame_per_second = 20
    playing = True
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    frame -= frame_per_second * 2
                    if frame < 0:
                        frame = 0
                if event.key == pygame.K_RIGHT:
                    frame += frame_per_second * 2
                if event.key == pygame.K_UP:
                    frame_per_second += 5
                    if frame_per_second == 6:
                        frame_per_second = 5
                if event.key == pygame.K_DOWN:
                    frame_per_second -= 5
                    if frame_per_second < 1:
                        frame_per_second = 1
                if event.key == pygame.K_SPACE:
                    playing = not playing
        if pipe_mode:
            # 读取管道
            pipe = open(pipe_path, "r")
            data = pipe.readline()
            pipe.close()
            data = data.strip().split()
            if len(data) == 12:
                draw(0, frame, data)
            frame += 1
        else:
            if frame < len(whole_data):
                data = whole_data[frame].strip().split()
                if len(data) == 12:
                    draw(frame_per_second, frame, data)
                if playing:
                    frame += 1
                    time.sleep(1 / frame_per_second)
