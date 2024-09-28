import pygame
import random
import time

# 初始化 Pygame
pygame.init()

# 初始化混音器
pygame.mixer.init()

# 点击音效
click_sound = pygame.mixer.Sound('qingliang_bgm/点击音效.wav')

# 加载消除成功的声音
match_sound = pygame.mixer.Sound('qingliang_bgm/connected ok.mp3')

# 播放音乐的函数
pygame.mixer.music.load('qingliang_bgm/主bgm.mp3')
pygame.mixer.music.play(-1)  # -1表示无限循环

# 定义常量
WIDTH, HEIGHT = 600, 600
TILE_SIZE = 80
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (200, 200, 200)
BUTTON_WIDTH, BUTTON_HEIGHT = 300, 100  # 按钮的宽高
GAME_TIME = 60  # 游戏时间（秒）
GAME_OVER_DELAY = 5  # 游戏结束后自动返回主菜单的延迟时间（秒）

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("清凉一夏")

# 加载背景图
background_image = pygame.image.load('test_pic\\background1.jpg')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# 加载图案图片
patterns = [pygame.image.load(f"test_pic\\image_{i}.jpg") for i in range(1, 11)]
patterns = [pygame.transform.scale(p, (TILE_SIZE, TILE_SIZE)) for p in patterns]

# 加载按钮图标（作为背景图），并调整比例
start_game_icon = pygame.image.load('test_pic\\button1.jpg')
scores_icon = pygame.image.load('test_pic\\button1.jpg')

start_game_icon = pygame.transform.scale(start_game_icon, (BUTTON_WIDTH, BUTTON_HEIGHT))

scores_icon = pygame.transform.scale(scores_icon, (BUTTON_WIDTH, BUTTON_HEIGHT))

# 按钮设置
button_font = pygame.font.Font(pygame.font.match_font('simhei'), 36)  # 使用支持中文的字体

# 加载成功和失败的图像
success_images = [pygame.image.load(f'test_pic/success{i}.jpg') for i in range(1, 4)]
fail_images = [pygame.image.load(f'test_pic/fail.jpg')]  # 假设失败图只有一张

# 加载说明书图片
instruction_image = pygame.image.load('test_pic/info.jpg')
instruction_image = pygame.transform.scale(instruction_image, (WIDTH, HEIGHT))  # 调整图片大小


def draw_end_screen(current_game, failed):
    screen.fill(BG_COLOR)
    if failed:  # 游戏失败
        image = fail_images[0]  # 只取失败图片
    else:  # 游戏成功
        image = success_images[current_game - 1]  # 获取当前局数的成功图片

    # 将图片缩放到适合屏幕的大小
    image = pygame.transform.scale(image, (WIDTH, HEIGHT))
    screen.blit(image, (0, 0))


def draw_blue_button(text, x, y, width, height):
    button_surface = pygame.Surface((width, height))  # 创建按钮表面
    button_surface.fill((0, 0, 255))  # 填充蓝色

    screen.blit(button_surface, (x, y))  # 绘制按钮背景

    # 绘制文本
    text_surface = button_font.render(text, True, (255, 255, 255))  # 白色字体
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)  # 绘制文本


def draw_button(text, x, y, width, height, icon):
    screen.blit(icon, (x, y))  # 绘制背景图
    text_surface = button_font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)


def draw_scores(scores):
    screen.fill(BG_COLOR)
    title_font = pygame.font.Font(pygame.font.match_font('simhei'), 48)
    title_surface = title_font.render("积分榜单", True, BLACK)
    title_rect = title_surface.get_rect(center=(WIDTH // 2, 50))
    screen.blit(title_surface, title_rect)

    scores_font = pygame.font.Font(pygame.font.match_font('simhei'), 36)
    y_offset = 100
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for idx, (player, score) in enumerate(sorted_scores):
        score_surface = scores_font.render(f"{idx + 1}. {player}: {score}", True, BLACK)
        score_rect = score_surface.get_rect(center=(WIDTH // 2, y_offset))
        screen.blit(score_surface, score_rect)
        y_offset += 50

    back_message = button_font.render("点击任意处返回主菜单", True, BLACK)
    back_rect = back_message.get_rect(center=(WIDTH // 2, HEIGHT - 60))
    screen.blit(back_message, back_rect)



def draw_message(message):
    screen.fill(BG_COLOR)
    message_font = pygame.font.Font(pygame.font.match_font('simhei'), 48)
    message_surface = message_font.render(message, True, BLACK)
    message_rect = message_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(message_surface, message_rect)
    restart_surface = button_font.render("点击任意处返回主菜单", True, BLACK)
    restart_rect = restart_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
    screen.blit(restart_surface, restart_rect)


def draw_final_scores(scores):
    screen.fill(BG_COLOR)
    title_font = pygame.font.Font(pygame.font.match_font('simhei'), 48)
    title_surface = title_font.render("最终成绩", True, BLACK)
    title_rect = title_surface.get_rect(center=(WIDTH // 2, 50))
    screen.blit(title_surface, title_rect)

    scores_font = pygame.font.Font(pygame.font.match_font('simhei'), 36)
    y_offset = 100
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)  # 按分数排序
    for idx, (player, score) in enumerate(sorted_scores):
        score_surface = scores_font.render(f"{idx + 1}. {player}: {score}", True, BLACK)
        score_rect = score_surface.get_rect(center=(WIDTH // 2, y_offset))
        screen.blit(score_surface, score_rect)
        y_offset += 50


def draw_board():
    global click_played  # 使用全局变量

    screen.blit(background_image, (0, 0))  # 重新绘制背景图
    for tile in sorted(tiles, key=lambda t: t['layer']):
        screen.blit(tile['image'], tile['rect'])

    # 绘制得分
    score_surface = button_font.render(f"得分: {score}", True, BLACK)
    screen.blit(score_surface, (10, 10))

    # 绘制倒计时
    current_time = time.time()
    elapsed_time = current_time - start_time
    remaining_time = max(GAME_TIME - int(elapsed_time), 0)
    timer_surface = button_font.render(f"时间: {remaining_time}", True, BLACK)
    screen.blit(timer_surface, (WIDTH - 150, 10))

    # 绘制被选中的方块的指示
    for tile in selected:
        pygame.draw.rect(screen, (0, 0, 255), tile['rect'], 3)  # 蓝色边框，宽度为3

    # 绘制小型加料按钮
    draw_blue_button("加料", 10, HEIGHT - 60, 80, 30)  # 小按钮

    draw_shuffle_button()


def add_tiles(current_game):
    global tiles
    num_pairs_to_add = 5  # 增加 5 对方块
    if current_game == 1:
        tiles += generate_additional_tiles(num_pairs_to_add, 2)  # 每对 2 块
    else:
        tiles += generate_additional_tiles(num_pairs_to_add, 3)  # 每对 3 块

def draw_shuffle_button():
    shuffle_button_x = WIDTH - 100  # 按钮的 X 坐标
    shuffle_button_y = HEIGHT - 60   # 按钮的 Y 坐标
    button_width, button_height = 80, 30  # 按钮大小
    draw_blue_button("洗牌", shuffle_button_x, shuffle_button_y, button_width, button_height)

def shuffle_tiles():
    global tiles
    remaining_tiles = len(tiles)  # 当前剩余方块数量

    if remaining_tiles > 0:
        # 清空当前方块
        tiles.clear()

        # 计算要生成的新对数
        if current_game == 1:
            num_pairs = (remaining_tiles // 2)  # 第一局生成 2 的倍数
            new_pairs = num_pairs  # 直接使用剩余方块数的对数
        else:
            num_pairs = (remaining_tiles // 3)  # 第二局和第三局生成 3 的倍数
            new_pairs = num_pairs * 3  # 每对生成三个

        if new_pairs > 0:
            # 生成新的方块
            patterns_to_use = random.sample(patterns, num_pairs)  # 随机选择图案
            for image in patterns_to_use:
                for _ in range(2 if current_game == 1 else 3):  # 第一局两块，其他局三块
                    x = random.randint(0, WIDTH - TILE_SIZE)
                    y = random.randint(0, HEIGHT - TILE_SIZE)
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    layer = random.randint(0, 1000)
                    tiles.append({'image': image, 'rect': rect, 'layer': layer})

        random.shuffle(tiles)  # 打乱方块顺序


def generate_board(current_game):
    if current_game == 1:
        num_pairs = 6  # 第一局生成 6 对 (12 个方块，2 的倍数)
    elif current_game == 2:
        num_pairs = 12  # 第二局生成 12 对 (36 个方块，3 的倍数)
    else:  # 第三局
        num_pairs = 15  # 第三局生成 15 对 (45 个方块，3 的倍数)

    if num_pairs > len(patterns):
        patterns_expanded = patterns * (num_pairs // len(patterns) + 1)
    else:
        patterns_expanded = patterns

    # 根据当前局数决定倍数
    multiplier = 2 if current_game == 1 else 3
    pattern_list = random.sample(patterns_expanded, num_pairs) * multiplier
    random.shuffle(pattern_list)

    tiles = []
    for _ in range(num_pairs * multiplier):
        image = pattern_list.pop()
        x = random.randint(0, WIDTH - TILE_SIZE)
        y = random.randint(0, HEIGHT - TILE_SIZE)
        rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        layer = random.randint(0, 1000)
        tiles.append({'image': image, 'rect': rect, 'layer': layer})

    return tiles



def check_match():
    global score
    if current_game == 1 and len(selected) == 2:  # 第一局，检查两个方块
        t1, t2 = selected
        if t1['image'] == t2['image']:  # 检查两个方块是否相同
            if t1 in tiles and t2 in tiles:  # 确保两个方块都在 tiles 中
                tiles.remove(t1)
                tiles.remove(t2)
                score += 10  # 每消除一对得 10 分
                match_sound.play()  # 播放匹配成功的音效
    elif current_game > 1 and len(selected) == 3:  # 第二局和第三局，检查三个方块
        t1, t2, t3 = selected
        if t1['image'] == t2['image'] == t3['image']:  # 检查三个方块是否相同
            if t1 in tiles and t2 in tiles and t3 in tiles:  # 确保三个方块都在 tiles 中
                tiles.remove(t1)
                tiles.remove(t2)
                tiles.remove(t3)
                score += 15  # 每消除三块得 15 分
                match_sound.play()  # 播放匹配成功的音效
    else:
        # 如果不匹配，稍后恢复图案（可选）
        pygame.time.wait(500)  # 等待 500 毫秒
    selected.clear()


def check_game_over():
    global game_over
    if len(tiles) == 0 or (time.time() - start_time) >= GAME_TIME:
        game_over = True
        return True
    return False




def generate_additional_tiles(num_pairs, tiles_per_pair):
    patterns_expanded = random.sample(patterns, num_pairs)  # 随机选择图案
    new_tiles = []
    for image in patterns_expanded:
        for _ in range(tiles_per_pair):
            x = random.randint(0, WIDTH - TILE_SIZE)
            y = random.randint(0, HEIGHT - TILE_SIZE)
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            layer = random.randint(0, 1000)
            new_tiles.append({'image': image, 'rect': rect, 'layer': layer})
    return new_tiles


def show_main_menu():
    screen.blit(background_image, (0, 0))
    draw_button("开始游戏", 150, 210, BUTTON_WIDTH, BUTTON_HEIGHT, start_game_icon)
    draw_button("查看积分排行", 150, 320, BUTTON_WIDTH, BUTTON_HEIGHT, scores_icon)
    draw_button("说明书", 150, 430, BUTTON_WIDTH, BUTTON_HEIGHT, start_game_icon)  # 说明书按钮

def handle_main_menu_click(mouse_x, mouse_y):
    start_button_rect = pygame.Rect(150, 250, BUTTON_WIDTH, BUTTON_HEIGHT)
    scores_button_rect = pygame.Rect(150, 370, BUTTON_WIDTH, BUTTON_HEIGHT)
    instructions_button_rect = pygame.Rect(150, 490, BUTTON_WIDTH, BUTTON_HEIGHT)  # 说明书按钮

    if start_button_rect.collidepoint(mouse_x, mouse_y):
        return 'start_game'
    elif scores_button_rect.collidepoint(mouse_x, mouse_y):
        return 'view_scores'
    elif instructions_button_rect.collidepoint(mouse_x, mouse_y):
        return 'view_instructions'  # 返回说明书
    return None





def reset_game():
    global game_active, showing_scores, game_over, final_scores_displayed, score, selected, current_game, tiles, player_name
    game_active = False
    showing_scores = False
    game_over = False
    final_scores_displayed = False
    score = 0
    selected = []
    current_game = 1  # 重置关卡
    tiles = generate_board(current_game)  # 生成新的方块
    player_name = ""



def update_scores(player_name, new_score):
    if player_name in scores:
        scores[player_name] += new_score
    else:
        scores[player_name] = new_score




def prompt_for_name():
    global player_name
    input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    font = pygame.font.Font(pygame.font.match_font('simhei'), 36)
    base_surface = pygame.Surface((WIDTH, HEIGHT))

    while True:
        base_surface.fill(BG_COLOR)
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        base_surface.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(base_surface, color, input_box, 2)
        screen.blit(base_surface, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                    color = color_active if active else color_inactive
                else:
                    active = False
                    color = color_active if active else color_inactive



# 游戏板和初始界面状态
replay_current_game = False  # 用于控制是否重玩当前局
game_active = False
showing_scores = False
game_over = False
final_scores_displayed = False
score = 0
selected = []

start_time = None
game_end_time = None
current_game = 1
total_games = 3
scores = {}  # 存储玩家积分的字典
player_name = ""
tiles = generate_board(current_game)
showing_instructions = False  # 新增变量


# 主游戏循环
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(FPS)

    if showing_instructions:  # 如果正在显示说明书
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()  # 播放点击音效
                showing_instructions = False  # 点击返回主菜单

        screen.blit(instruction_image, (0, 0))  # 显示说明书
        pygame.display.flip()
        continue  # 跳过其余的循环

    if game_active:
        if check_game_over():
            game_active = False
            game_over = True
            game_end_time = time.time()  # 记录游戏结束时间
            failed = len(tiles) > 0  # 设置失败标志

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            click_sound.play()  # 在任何地方点击时播放音效



            if not game_active and not showing_scores and game_over:
                if failed:
                    score = 0  # 清空当前局的得分
                    score -= 100  # 扣除 100 分
                    tiles = generate_board(current_game)  # 重新生成当前局的方块
                    game_active = True
                    start_time = time.time()  # 重新开始计时
                else:
                    # 进入下一关
                    update_scores(player_name, score)  # 更新分数
                    current_game += 1
                    if current_game <= total_games:
                        game_active = True
                        start_time = time.time()  # 记录游戏开始时间
                        tiles = generate_board(current_game)  # 生成新的方块
                    else:
                        reset_game()  # 返回主菜单



            elif not game_active and showing_scores:
                # 点击积分榜返回主菜单
                reset_game()  # 重置游戏状态，返回主菜单

            elif not game_active and not showing_scores and not game_over:
                action = handle_main_menu_click(mouse_x, mouse_y)
                if action == 'start_game':
                    player_name = prompt_for_name()  # 提示玩家输入姓名
                    game_active = True
                    start_time = time.time()  # 记录游戏开始时间
                    tiles = generate_board(current_game)  # 生成方块
                elif action == 'view_scores':
                    showing_scores = True
                elif action == 'view_instructions':  # 新增说明书逻辑
                    showing_instructions = True
            elif game_active:

                clicked_tile = next((t for t in tiles if t['rect'].collidepoint(mouse_x, mouse_y)), None)
                if clicked_tile and clicked_tile not in selected:
                    selected.append(clicked_tile)
                    if len(selected) == (3 if current_game > 1 else 2):  # 根据关卡选择方块数
                        check_match()

                # 检查加料按钮是否被点击
                add_button_rect = pygame.Rect(10, HEIGHT - 100, BUTTON_WIDTH // 2, BUTTON_HEIGHT // 2)
                if add_button_rect.collidepoint(mouse_x, mouse_y):
                    add_tiles(current_game)  # 调用加料函数


                # 检查洗牌按钮是否被点击
                shuffle_button_rect = pygame.Rect(WIDTH - 100, HEIGHT - 60, 80, 30)
                if shuffle_button_rect.collidepoint(mouse_x, mouse_y):
                    shuffle_tiles()  # 调用洗牌功能

    if game_active:
        draw_board()
    elif showing_scores:
        draw_scores(scores)  # 显示积分榜
    elif game_over:
        draw_end_screen(current_game, failed)  # 根据当前局数显示相应的结束界面
    else:
        show_main_menu()

    pygame.display.flip()

# 停止音乐并退出
pygame.mixer.music.stop()
pygame.quit()
