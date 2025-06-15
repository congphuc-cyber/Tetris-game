import pygame
import random

pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 30 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height


# SHAPE FORMATS

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape


class Piece(object):  # *
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_pos={}):  # *
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j,i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


def get_shape():
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width /2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))


def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_size), (sx+play_width, sy+ i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j*block_size, sy),(sx + j*block_size, sy + play_height))


def clear_rows(grid, locked):

    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))


def update_score(nscore):
    score = max_score()

    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score


def draw_window(surface, grid, score=0, last_score = 0):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return  # Thoát khỏi hàm draw_window nếu cửa sổ bị đóng
    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    # current score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100

    surface.blit(label, (sx + 20, sy + 160))
    # last score
    label = font.render('High Score: ' + last_score, 1, (255,255,255))

    sx = top_left_x - 250
    sy = top_left_y + 200

    surface.blit(label, (sx + 20, sy + 160))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

    draw_grid(surface, grid)
    #pygame.display.update()
    
def main(win, name_input):  # Thêm tham số name_input
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  # Dừng vòng lặp khi cửa sổ bị đóng
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        # Chỉ gọi draw_window nếu cửa sổ còn mở
        if run:
            draw_window(win, grid, score, last_score)
            draw_next_shape(next_piece, win)
            pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle(win, "YOU LOST!", 80, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score)

    pygame.quit()  # Gọi pygame.quit() khi chương trình kết thúc

def main_menu(win):  # *
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  # Dừng vòng lặp khi cửa sổ bị đóng
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Kiểm tra nếu chuột nhấn vào một nút
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if play_button.collidepoint(mouse_x, mouse_y):  # Chơi ngay
                    run = False
                    enter_name_screen(win)  # Màn hình nhập tên
                elif rank_button.collidepoint(mouse_x, mouse_y):  # Bảng xếp hạng
                    show_high_scores(win)  # Hiển thị bảng xếp hạng
                elif quit_button.collidepoint(mouse_x, mouse_y):  # Thoát
                    run = False

        # Vẽ giao diện menu
        draw_main_menu(win)
        pygame.display.update()

def enter_name_screen(win):
    run = True
    name_input = ""  # Tên người chơi
    font = pygame.font.SysFont('comicsans', 40)
    input_rect = pygame.Rect(top_left_x + play_width / 2 - 150, top_left_y + play_height / 2 - 30, 300, 50)
    start_button = pygame.Rect(top_left_x + play_width / 2 - 100, top_left_y + play_height / 2 + 50, 200, 50)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    name_input = name_input[:-1]  # Xóa ký tự cuối cùng
                elif event.key == pygame.K_RETURN and name_input != "":
                    # Khi nhấn Enter và có tên, bắt đầu game
                    main(win, name_input)
                    run = False  # Dừng màn hình nhập tên
                elif event.key != pygame.K_RETURN:
                    name_input += event.unicode  # Thêm ký tự vào tên

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Kiểm tra nếu chuột nhấn vào nút "Bắt đầu"
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if start_button.collidepoint(mouse_x, mouse_y) and name_input != "":
                    main(win, name_input)  # Chuyển vào game khi nhấn "Bắt đầu"
                    run = False  # Dừng màn hình nhập tên
                elif start_button.collidepoint(mouse_x, mouse_y) and name_input == "":
                    # Thêm một thông báo khi chưa nhập tên
                    print("Vui lòng nhập tên trước khi bắt đầu!")  # Có thể thay bằng thông báo trong game

        win.fill((0, 0, 0))  # Nền đen
        draw_text_middle(win, 'Nhập tên của bạn:', 40, (255, 255, 255))

        # Vẽ ô nhập tên
        pygame.draw.rect(win, (255, 255, 255), input_rect)
        text_surface = font.render(name_input, True, (0, 0, 0))
        win.blit(text_surface, (input_rect.x + 10, input_rect.y + 10))

        # Vẽ nút bắt đầu
        pygame.draw.rect(win, (0, 255, 0), start_button)
        start_text = font.render('Bắt đầu', True, (255, 255, 255))
        win.blit(start_text, (start_button.x + (start_button.width - start_text.get_width()) / 2, start_button.y + (start_button.height - start_text.get_height()) / 2))

        pygame.display.update()


def draw_main_menu(surface):
    surface.fill((0, 0, 0))  # Đặt nền màu đen

    font = pygame.font.SysFont('comicsans', 60)
    title = font.render('TETRIS', 1, (255, 255, 255))
    surface.blit(title, (top_left_x + play_width / 2 - title.get_width() / 2, top_left_y + 50))

    # Tạo nút cho ba lựa chọn
    button_width = 200
    button_height = 50
    button_x = top_left_x + play_width / 2 - button_width / 2
    button_y_start = top_left_y + play_height / 2 - 100
    button_spacing = 60

    # Tạo các nút
    global play_button, rank_button, quit_button

    play_button = pygame.Rect(button_x, button_y_start, button_width, button_height)
    rank_button = pygame.Rect(button_x, button_y_start + button_spacing, button_width, button_height)
    quit_button = pygame.Rect(button_x, button_y_start + 2 * button_spacing, button_width, button_height)

    pygame.draw.rect(surface, (255, 0, 0), play_button)
    pygame.draw.rect(surface, (0, 255, 0), rank_button)
    pygame.draw.rect(surface, (0, 0, 255), quit_button)

    font = pygame.font.SysFont('comicsans', 30)
    play_text = font.render('Chơi Ngay', 1, (255, 255, 255))
    rank_text = font.render('Bảng Xếp Hạng', 1, (255, 255, 255))
    quit_text = font.render('Thoát', 1, (255, 255, 255))

    surface.blit(play_text, (play_button.x + (play_button.width - play_text.get_width()) / 2, play_button.y + (play_button.height - play_text.get_height()) / 2))
    surface.blit(rank_text, (rank_button.x + (rank_button.width - rank_text.get_width()) / 2, rank_button.y + (rank_button.height - rank_text.get_height()) / 2))
    surface.blit(quit_text, (quit_button.x + (quit_button.width - quit_text.get_width()) / 2, quit_button.y + (quit_button.height - quit_text.get_height()) / 2))


def show_high_scores(win):
    # Sử dụng hàm max_score() để lấy điểm cao nhất
    high_score = max_score()

    # Hiển thị bảng xếp hạng
    win.fill((0, 0, 0))  # Đặt nền màu đen
    draw_text_middle(win, 'Bảng Xếp Hạng', 60, (255, 255, 255))

    font = pygame.font.SysFont('comicsans', 40)
    label = font.render(f'High Score: {high_score}', 1, (255, 255, 255))
    win.blit(label, (top_left_x + play_width / 2 - label.get_width() / 2, top_left_y + play_height / 2 - label.get_height() / 2))

    pygame.display.update()
    pygame.time.delay(3000)  # Hiển thị bảng xếp hạng trong 3 giây
    main_menu(win)  # Quay lại menu chính sau khi xem bảng xếp hạng

    
win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)