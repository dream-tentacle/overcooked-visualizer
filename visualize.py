"""介绍：
使用pygame进行可视化速度和移动方向
该项目需要创建临时文件，并需要提供地图文件，请自行修改以下代码中的
`tmp_root` 和 `map_root`

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

python3 visualize.py <LVL> <MODE>
- <LVL> 是关卡名称 (例如 "1-1")
- <MODE> 是 0 或 1. 
    0 表示 log 模式, 1 表示管道模式

按左右键可以快进快退，按上下键可以调整帧率，空格可以暂停，并可以拖动进度条

# 要求：
管道模式下,先运行该文件,再运行 QtOvercooked, 在QtOvercooked中每一帧按照上述格式写入管道
log 模式下,先运行 QtOvercooked, 在 QtOvercooked 中每一帧按照上述格式写入一行到log.txt
见提供的 plugin.cpp 文件

"""

import pygame
import sys
import os
import time

# modify these as needed.
tmp_root = "/tmp"
map_root = "./maps"


# do not modify the following params.
if not os.path.exists(f"{tmp_root}/visualize"):
    os.makedirs(f"{tmp_root}/visualize")

pipe_path = f"{tmp_root}/visualize/pipe"
log_path = f"{tmp_root}/visualize/log.txt"

map_ = [".........." for _ in range(10)]


def read_map(lvl):
    x, _ = lvl.split("-")
    with open(f"{map_root}/level{x}/level{lvl}.txt") as file:
        # find the 2-11 lines of the file and store them in map_
        file.readline()
        global map_
        map_ = ["" for _ in range(10)]
        for i in range(10):
            map_[i] = file.readline().strip()


def draw(speed, frame, data: list, maxframe=14400):
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
    light_red = (255, 200, 200)
    light_green = (200, 255, 200)
    gray = (128, 128, 128)
    dark_gray = (64, 64, 64)
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
    # 绘制地图
    for i in range(0, maxwidth):
        for j in range(0, maxheight):
            if map_[j][i] != ".":
                pygame.draw.rect(
                    screen,
                    dark_gray,
                    (
                        i * width / maxwidth + margin / 2,
                        j * height / maxheight + margin / 2,
                        width / maxwidth,
                        height / maxheight,
                    ),
                    0,
                )
    # 绘制角色位置
    pygame.draw.circle(screen, light_red, position1, 0.35 * block_size)
    pygame.draw.circle(screen, light_green, position2, 0.35 * block_size)
    # 在角色周围绘制移动
    pygame.draw.circle(
        screen,
        dark_red,
        (move1[0] + position1[0], move1[1] + position1[1]),
        10,
    )
    pygame.draw.circle(
        screen,
        dark_green,
        (move2[0] + position2[0], move2[1] + position2[1]),
        10,
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
    # 绘制frame和maxframe的比例
    pygame.draw.rect(
        screen,
        gray,
        (margin / 2, 10, width, 20),
        0,
    )
    pygame.draw.rect(
        screen,
        dark_gray,
        (margin / 2, 10, width * frame / maxframe, 20),
        0,
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
        f"({str(p1x)[:4]},{str(p1y)[:4]}) ({str(v1x)[:4]},\
        {str(v1y)[:4]}) ({str(a1x)[:4]},{str(a1y)[:4]}) red",
        1,
        (10, 10, 10),
    )
    screen.blit(text, (10, height + margindown + 10))
    text = font.render(
        f"({str(p2x)[:4]},{str(p2y)[:4]}) ({str(v2x)[:4]},\
        {str(v2y)[:4]}) ({str(a2x)[:4]},{str(a2y)[:4]}) green",
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
    if len(sys.argv) != 3:
        print("""Usage: python3 visualize.py <LVL> <MODE>
\t- <LVL> is the level number. (e.g. \"1-1\")
\t- <MODE> is either 0 or 1; 0 for log mode, 1 for pipe mode.""")
        sys.exit(1)
    lvl = sys.argv[1]
    read_map(lvl)
    pipe_mode = sys.argv[2] == "1"
    # 管道路径
    if pipe_mode:
        # 先删除管道
        if os.path.exists(pipe_path):
            os.remove(pipe_path)
        # 创建管道
        create_pipe(pipe_path)
    else:
        with open(log_path, "r") as f:
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
    block_size = 1.0 * width / maxwidth
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
            if event.type == pygame.KEYDOWN and not pipe_mode:
                if event.key == pygame.K_LEFT:
                    frame -= frame_per_second * 2
                    if frame < 0:
                        frame = 0
                if event.key == pygame.K_RIGHT:
                    frame += frame_per_second * 2
                    if frame >= len(whole_data):
                        frame = len(whole_data) - 1
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
            print(data)
            data = data.strip().split()
            if len(data) == 12:
                draw(0, frame, data)
            frame += 1
        else:
            # 检测鼠标点击
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if pos[1] < margin / 2:
                    frame = int((pos[0] - margin / 2) /
                                width * len(whole_data))
                    if frame >= len(whole_data):
                        frame = len(whole_data) - 1
            data = whole_data[frame].strip().split()
            if len(data) == 12:
                draw(frame_per_second, frame, data, len(whole_data))
            if playing:
                if frame < len(whole_data) - 1:
                    frame += 1
                time.sleep(1 / frame_per_second)
