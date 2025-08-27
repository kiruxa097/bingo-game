# --------- BACKEND ---------

# стандартные библиотеки:
import math
import random

# сторонние библиотеки:
import pygame

def choice_size_card(size):  # функция для выбора и создания карточки игрока
    card_player = []  # карточка игрока
    line = []
    check_repeats = set()
    for _ in range(size):
        for _ in range(size):  # линия с рандом значениями
            digit = random.randint(1, 75)  # создаем новое число в карточку
            while digit in check_repeats:  # проверяем на совпадения с предыдущими числами
                digit = random.randint(1, 75)
            line.append(digit)
            check_repeats.add(digit)
        card_player.append(line) # добавляем линии в карточку
        line = []  # чистим список перед переходом на новую линию
    return card_player, check_repeats

def generation_digit_barrel(size, repeat, card_player):  # функция для генерации чисел при взятии бочонка
    set_all_digit = set()  # множество с выпавшими уже числами
    set_digit_on_barrel = set()  # множество с выпавшими и совпавшими на карточке числами
    repeat = set(repeat)
    while len(set_digit_on_barrel) != size*size:  # достаем числа из бочонка пока все числа на карточке на закроются
        digit = random.randint(1,75)
        if digit not in set_all_digit:
            yield digit  # возвращаем выпавшее число
            if digit in repeat:  # проверяем число на совпадение с числами на карточке
                set_digit_on_barrel.add(digit)
                for line in range(len(card_player)):  # проходимся по линиям и проверяем есть ли такое число
                    if digit in card_player[line]:
                        card_player[line][card_player[line].index(digit)] = "X"
                        yield card_player
            set_all_digit.add(digit)

#  ------FRONTED-------

# инициализация pygame
pygame.init()

# размер окна игры
width, height = 1200, 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("BINGO")
image = pygame.image.load("window_bingo.png").convert_alpha()
image_singl_menu_6x6 = pygame.image.load("singl_menu_6x6.png").convert_alpha()
image_singl_menu_4x4 = pygame.image.load("singl_menu_4x4.png").convert_alpha()
image_singl_menu_5x5 = pygame.image.load("single_menu_5x5.png").convert_alpha()
background_color = (255, 243, 176)
run = True
menu_state = "main"

# кнопки
button_rect, button_first_menu, button_rect_for_exit, button_rect_beh1, button_rect_beh2, button_rect2, button_4x4, button_5x5, button_6x6 = None, None, None, None, None, None, None, None, None
curret_card = None
current_number = None
# Функция для текста с контуром
def draw_text_with_outline(surface, text, font, color, outline_color, center_pos, outline_width=2):
    text_surf = font.render(text, True, color)
    # Рисуем контур
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                outline_surf = font.render(text, True, outline_color)
                outline_rect = outline_surf.get_rect(center=(center_pos[0]+dx, center_pos[1]+dy))
                surface.blit(outline_surf, outline_rect)
    text_rect = text_surf.get_rect(center=center_pos)
    surface.blit(text_surf, text_rect)

# функция для рисовки кнопок
def draw_window_button(button_color, button_x, button_y, button_widht, button_height):
    button_rect = pygame.Rect(0, 0, button_widht, button_height)
    button_rect.center = (button_x, button_y)
    pygame.draw.rect(window, button_color, button_rect, border_radius=20)
    pygame.draw.rect(window, (48, 30, 19), button_rect, width=1, border_radius=20)
    return button_rect

# функция для рисовки ячеек карточки игрока
def draw_bingo_card(surface, card, start_x, start_y):
    font = pygame.font.SysFont(None, 40)
    cell_size = 100
    margin = 10
    cell_color = (224, 159, 62)
    line_color = (48, 30, 19)
    text_color = (0, 0, 0)

    for i, row in enumerate(card):
        for j, num in enumerate(row):
            x = start_x + j * (cell_size + margin)
            y = start_y + i * (cell_size + margin)
            rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(surface, cell_color, rect, border_radius=10)
            pygame.draw.rect(surface, line_color, rect, width=3, border_radius=10)
            text_surf = font.render(str(num), True, text_color)
            text_rect = text_surf.get_rect(center=rect.center)
            surface.blit(text_surf, text_rect)

# основной цикл игры

while run:
    if menu_state == "main":  # рисуем кнопки и фон
        window.fill(background_color)
        window.blit(image, (-75, -80))
        button_rect = draw_window_button((61, 43, 31), width // 2, height // 2, 300, 100)
        button_rect_for_exit = draw_window_button((61, 43, 31), width // 2, 520, 300, 100)
    elif menu_state == "mode_selection":  # рисуем кнопки и фон
        window.fill(background_color)
        window.blit(image, (-75, -80))
        button_rect = draw_window_button((61, 43, 31), width // 2, height // 2, 300, 100)
        button_rect2 = draw_window_button((61, 43, 31), width // 2, 520, 300, 100)
        button_rect_beh1 = draw_window_button((61, 43, 31), width // 2, 640, 300, 100)
    elif menu_state == "single_game_mode":  # рисуем кнопки и фон
        window.fill(background_color)
        window.blit(image, (-75, -80))
        button_4x4 = draw_window_button((61, 43, 31), width // 2, 325, 210, 65)
        button_5x5 = draw_window_button((61, 43, 31), width // 2, 400, 210, 65)
        button_6x6 = draw_window_button((61, 43, 31), width // 2, 475, 210, 65)
        button_rect_beh2 = draw_window_button((61, 43, 31), width // 2, 550, 210, 65)
    elif menu_state == "single_game_mode_4x4":  # рисуем кнопки и фон
        window.fill(background_color)
        window.blit(image_singl_menu_4x4, (-75, -80))
        if curret_card:
            pygame.draw.rect(window, (48, 30, 19), (140, 140, 450, 450), 4)  # контур ячеек с числами
            pygame.draw.circle(window, (48, 30, 19), (900, 370), 115, 8)  # круг, в котором будут числа

            draw_bingo_card(window, curret_card, start_x=150, start_y=150)

            # показываем число внутри круга
            if current_number is not None:
                font_circle = pygame.font.SysFont("Verdana", 80, bold=True)
                text_surface = font_circle.render(str(current_number), True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(900, 370))
                window.blit(text_surface, text_rect)

    elif menu_state == "single_game_mode_5x5":
        window.fill(background_color)
        window.blit(image_singl_menu_5x5, (-75, -80))
        if curret_card:
            pygame.draw.rect(window, (48, 30, 19), (140, 140, 560, 560), 4)  # контур ячеек с числами
            pygame.draw.circle(window, (48, 30, 19), (950, 370), 115, 8)  # круг, в котором будут числа

            draw_bingo_card(window, curret_card, start_x=150, start_y=150)

            # показываем число внутри круга
            if current_number is not None:
                font_circle = pygame.font.SysFont("Verdana", 80, bold=True)
                text_surface = font_circle.render(str(current_number), True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(950, 370))
                window.blit(text_surface, text_rect)

    elif menu_state == "single_game_mode_6x6":
        window.fill(background_color)
        window.blit(image_singl_menu_6x6, (-75, -80))
        if curret_card:
            pygame.draw.rect(window, (48, 30, 19), (90, 90, 670, 670), 4)  # контур ячеек с числами
            pygame.draw.circle(window, (48, 30, 19), (975, 390), 115, 8)  # круг, в котором будут числа

            draw_bingo_card(window, curret_card, start_x=100, start_y=100)

            # показываем число внутри круга
            if current_number is not None:
                font_circle = pygame.font.SysFont("Verdana", 80, bold=True)
                text_surface = font_circle.render(str(current_number), True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(975, 390))
                window.blit(text_surface, text_rect)
    elif menu_state == "final_menu":
        window.fill(background_color)
        window.blit(image, (-75, -80))
        button_first_menu = draw_window_button((61, 43, 31), width // 2, 350, 300, 100)
        button_rect_for_exit = draw_window_button((61, 43, 31), width // 2, 475, 300, 100)

    # обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if menu_state == "main" and button_rect and button_rect.collidepoint(event.pos):
                if button_rect and button_rect.collidepoint(event.pos):
                    menu_state = "mode_selection"
            elif menu_state == "main" and button_rect_for_exit and button_rect_for_exit.collidepoint(event.pos):
                if button_rect_for_exit and button_rect_for_exit.collidepoint(event.pos):
                    pygame.quit()
            elif menu_state == "mode_selection":
                if button_rect and button_rect.collidepoint(event.pos):
                    menu_state = "single_game_mode"
                if button_rect_beh1 and button_rect_beh1.collidepoint(event.pos):
                    menu_state = "main"
            elif menu_state == "single_game_mode":
                if button_4x4 and button_4x4.collidepoint(event.pos):
                    menu_state = "single_game_mode_4x4"
                    curret_card, repeat_set = choice_size_card(4)
                    digit_generator = generation_digit_barrel(4, repeat_set, curret_card)
                    current_number = None
                elif button_5x5 and button_5x5.collidepoint(event.pos):
                    menu_state = "single_game_mode_5x5"
                    curret_card, repeat_set = choice_size_card(5)
                    digit_generator = generation_digit_barrel(5, repeat_set, curret_card)
                    current_number = None
                elif button_6x6 and button_6x6.collidepoint(event.pos):
                    menu_state = "single_game_mode_6x6"
                    curret_card, repeat_set = choice_size_card(6)
                    digit_generator = generation_digit_barrel(6, repeat_set, curret_card)
                    current_number = None
                elif button_rect_beh2 and button_rect_beh2.collidepoint(event.pos):
                    menu_state = "mode_selection"
            elif menu_state == "single_game_mode_4x4":
                # проверяем клик по кругу, который выдает числа
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if ((900 - event.pos[0]) ** 2 + (370 - event.pos[1]) ** 2) <= 115 ** 2:
                        if digit_generator:
                            try:
                                result = next(digit_generator)
                                if isinstance(result, list):
                                        curret_card = result
                                else:
                                    current_number = result  # сохраняем число
                                # проверка заполнения карточки
                                if all(cell == "X" for row in curret_card for cell in row):
                                    menu_state = "final_menu"
                            except StopIteration:
                                current_number = None  # если числа закончились
            elif menu_state == "single_game_mode_5x5":
                # проверяем клик по кругу, который выдает числа
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if ((950 - event.pos[0]) ** 2 + (370 - event.pos[1]) ** 2) <= 115 ** 2:
                        if digit_generator:
                            try:
                                result = next(digit_generator)
                                if isinstance(result, list):
                                        curret_card = result
                                else:
                                    current_number = result  # сохраняем число
                                # проверка заполнения карточки
                                if all(cell == "X" for row in curret_card for cell in row):
                                    menu_state = "final_menu"
                            except StopIteration:
                                current_number = None  # если числа закончились
            elif menu_state == "single_game_mode_6x6":
                # проверяем клик по кругу, который выдает числа
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if ((975 - event.pos[0]) ** 2 + (390 - event.pos[1]) ** 2) <= 115 ** 2:
                        if digit_generator:
                            try:
                                result = next(digit_generator)
                                if isinstance(result, list):
                                        curret_card = result
                                else:
                                    current_number = result  # сохраняем число
                                # проверка заполнения карточки
                                if all(cell == "X" for row in curret_card for cell in row):
                                    menu_state = "final_menu"
                            except StopIteration:
                                current_number = None  # если числа закончились
            elif menu_state == "final_menu":
                if button_first_menu and button_first_menu.collidepoint(event.pos):
                    menu_state = "main"
                if button_rect_for_exit and button_rect_for_exit.collidepoint(event.pos):
                    pygame.quit()
    # создание текстов в разных меню

    # создание текста на главном меню

    if menu_state == "main":
        font_for_welcome_text = pygame.font.SysFont("Verdana", 72, bold=True)
        font_for_button = pygame.font.SysFont("Verdana", 50, bold=True)
        font_for_welcome_under = pygame.font.SysFont("Verdana", 20, bold=True)
        color_for_button_text =  (255, 223, 132)
        welcome_color = (255, 223, 132)
        outline_welcom_color = (100, 64, 15)
        draw_text_with_outline(window, "ИГРАЙ", font_for_welcome_text, welcome_color, outline_welcom_color, center_pos=(width//2, 159), outline_width=3)
        draw_text_with_outline(window, "В BINGO!", font_for_welcome_text, welcome_color, outline_welcom_color, center_pos=(width // 2, 225),outline_width=3)
        draw_text_with_outline(window, "СТАРТ!", font_for_button, color_for_button_text, outline_welcom_color, center_pos=(600, 400), outline_width=1)
        draw_text_with_outline(window, "ВЫХОД", font_for_button, color_for_button_text, outline_welcom_color, center_pos=(600, 520), outline_width=1)

    # создание текста в меню выбора режима

    elif menu_state == "mode_selection":
        font_mode = pygame.font.SysFont("Verdana", 60, bold=True)
        welcome_color = (255, 223, 132)
        outline_welcom_color = (100, 64, 15)
        draw_text_with_outline(window, "ВЫБИРАЙ РЕЖИМ", font_mode, welcome_color, outline_welcom_color, center_pos=(width//2, 225), outline_width=3)
        font = pygame.font.Font(None, 36)
        draw_text_with_outline(window, "ОДИНОЧНЫЙ", font, welcome_color, outline_welcom_color, center_pos=(600, 400), outline_width=0)
        draw_text_with_outline(window, "С БОТОМ", font, welcome_color, outline_welcom_color, center_pos=(600, 510), outline_width=0)
        draw_text_with_outline(window, "(в разработке)", font, welcome_color, outline_welcom_color, center_pos=(600, 530), outline_width=0)
        draw_text_with_outline(window, "НАЗАД", font, welcome_color, outline_welcom_color, center_pos=(600, 640), outline_width=0)

    # создание текста в меню выбора режима

    elif menu_state == "single_game_mode":
        font_mode = pygame.font.SysFont("Verdana", 60, bold=True)
        font_mode_for_mode = pygame.font.SysFont("Verdana", 36, bold=True)
        color_title_text = (255, 223, 132)
        outline_title_color = (100, 64, 15)
        draw_text_with_outline(window, "КАКОЙ РАЗМЕР КАРТЫ?", font_mode, color_title_text, outline_title_color, center_pos=(width // 2, 190), outline_width=3)
        draw_text_with_outline(window, "4x4", font_mode_for_mode, color_title_text, outline_title_color, center_pos=(width // 2, 325), outline_width=1)
        draw_text_with_outline(window, "5x5", font_mode_for_mode, color_title_text, outline_title_color, center_pos=(width // 2, 400), outline_width=1)
        draw_text_with_outline(window, "НАЗАД", font_mode_for_mode, color_title_text, outline_title_color, center_pos=(width // 2, 550), outline_width=1)
        draw_text_with_outline(window, "6x6", font_mode_for_mode, color_title_text, outline_title_color, center_pos=(width // 2, 475), outline_width=1)

    # создание текста на карточке и круге в режиме 4х4

    elif menu_state == "single_game_mode_4x4":
        font_mode = pygame.font.SysFont("Verdana", 60, bold=True)
        font_mode_for_digit = pygame.font.SysFont("Verdana", 36, bold=True)
        color_title_text = (255, 223, 132)
        outline_title_color = (100, 64, 15)
        draw_text_with_outline(window, "Твоя карточка:", font_mode, color_title_text, outline_title_color, center_pos=(300, 75), outline_width=3)
        draw_text_with_outline(window, "ЖМИ", font_mode_for_digit, color_title_text, outline_title_color, center_pos=(900, 440), outline_width=3)
        draw_text_with_outline(window, "ЖМИ", font_mode_for_digit, color_title_text, outline_title_color, center_pos=(900, 300), outline_width=3)

    # создание текста на карточке и круге в режиме 5х5

    elif menu_state == "single_game_mode_5x5":
        font_mode = pygame.font.SysFont("Verdana", 60, bold=True)
        font_mode_for_digit = pygame.font.SysFont("Verdana", 36, bold=True)
        color_title_text = (255, 223, 132)
        outline_title_color = (100, 64, 15)
        draw_text_with_outline(window, "Твоя карточка:", font_mode, color_title_text, outline_title_color, center_pos=(300, 75), outline_width=3)
        draw_text_with_outline(window, "ЖМИ", font_mode_for_digit, color_title_text, outline_title_color, center_pos=(950, 440), outline_width=3)
        draw_text_with_outline(window, "ЖМИ", font_mode_for_digit, color_title_text, outline_title_color, center_pos=(950, 300), outline_width=3)

    # создание текста на карточке и круге в режиме 6х6

    elif menu_state == "single_game_mode_6x6":
        font_mode = pygame.font.SysFont("Verdana", 60, bold=True)
        font_mode_for_digit = pygame.font.SysFont("Verdana", 36, bold=True)
        color_title_text = (255, 223, 132)
        outline_title_color = (100, 64, 15)
        draw_text_with_outline(window, "Твоя карточка:", font_mode, color_title_text, outline_title_color, center_pos=(300, 45), outline_width=3)
        draw_text_with_outline(window, "ЖМИ", font_mode_for_digit, color_title_text, outline_title_color, center_pos=(975, 460), outline_width=3)
        draw_text_with_outline(window, "ЖМИ", font_mode_for_digit, color_title_text, outline_title_color, center_pos=(975, 320), outline_width=3)
    elif menu_state == "final_menu":
        image = pygame.image.load("window_bingo.png").convert_alpha()
        font = pygame.font.SysFont("Verdana", 54, bold=True)
        font_for_but1 = pygame.font.SysFont("Verdana", 30, bold=True)
        font_for_but2 = pygame.font.SysFont("Verdana", 36, bold=True)
        color_title_text = (255, 223, 132)
        outline_title_color = (100, 64, 15)
        draw_text_with_outline(window, "ПОЗДРАВЛЯЕМ!", font, color_title_text, outline_title_color, center_pos=(600, 100), outline_width=3)
        draw_text_with_outline(window, "ВЫ ЗАКРЫЛИ ВСЮ КАРТОЧКУ", font, color_title_text, outline_title_color, center_pos=(600, 175), outline_width=3)
        draw_text_with_outline(window, "ГЛАВНОЕ МЕНЮ", font_for_but1, color_title_text, outline_title_color, center_pos=(600, 350), outline_width=0)
        draw_text_with_outline(window, "ВЫХОД", font_for_but2, color_title_text, outline_title_color, center_pos=(600, 475), outline_width=0)

    pygame.display.flip()

pygame.quit()
