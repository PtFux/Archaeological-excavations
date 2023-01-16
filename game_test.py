import pygame
import random
from time import sleep
import sys
from os import path


class Point:
    point_set = set()
    count = 0
    score = 0
    max_point_size = 40

    def __init__(self, position_x=None, position_y=None, size=None):
        global MAX_X
        global MAX_Y

        if size is None:
            size = random.randint(3, Point.max_point_size)
        if position_x is None:
            position_x = random.randint(size, MAX_X - size)
        if position_y is None:
            position_y = random.randint(size, MAX_Y - size)

        self.position_x = position_x
        self.position_y = position_y
        self.size = size

        self.image = pygame.image.load(path.join(DIR_ALL,f'new_point{random.randint(1, 4)}.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (size, size))

        Point.point_set.add(self)

    def create(self):
        Point.count += 1
        screen.blit(self.image, (self.position_x, self.position_y))

    def draw(self):
        screen.blit(self.image, (self.position_x, self.position_y))

    def remove(self):
        Point.count -= 1
        if self.size > Point.max_point_size // 2 + Point.max_point_size // 3:
            bonus = Point.max_point_size // 8 * 3
        elif self.size > Point.max_point_size // 2:
            bonus = Point.max_point_size // 4
        elif self.size > Point.max_point_size // 3:
            bonus = Point.max_point_size // 8
        else:
            bonus = 1
        Point.score += bonus
        Point.point_set.remove(self)


class Player:
    cheat = False
    score_record = 0
    score_max = 0

    def __init__(self, x=None, y=None):
        global MAX_X
        global MAX_Y
        global SIZE_X
        global SIZE_Y

        if x is None:
            x = random.randint(SIZE_X, MAX_X - SIZE_X)
        if y is None:
            y = random.randint(SIZE_Y, MAX_Y - SIZE_Y)

        self.position_x = x
        self.position_y = y
        self.image = 'player0.png'
        self.image = path.join(DIR_ALL, self.image)
        self.image = pygame.image.load(self.image).convert()
        self.image = pygame.transform.scale(self.image, (SIZE_X, SIZE_Y))
        self.step = 5

        self.move_right = False
        self.move_left = False
        self.move_up = False
        self.move_down = False

        def create_mini_array(x_mini):
            return list(x_mini.split())

        with open('rating_user.txt', 'r') as f:
            array_score = list(map(create_mini_array, f.read().split('\n')))
            Player.score_max = int(array_score[1][1])

    def motion_player(self):
        global MAX_X
        global MAX_Y
        global SIZE_X
        global SIZE_Y

        if self.move_left:
            self.position_x += self.step
            if self.position_x > MAX_X:
                self.position_x = -SIZE_X

        if self.move_right:
            self.position_x -= self.step
            if self.position_x < -SIZE_X:
                self.position_x = MAX_X

        if self.move_up:
            self.position_y -= self.step
            if self.position_y < -SIZE_Y:
                self.position_y = MAX_Y

        if self.move_down:
            self.position_y += self.step
            if self.position_y > MAX_Y:
                self.position_y = -SIZE_Y

    def event_player(self, my_event):
        if my_event.type == pygame.KEYDOWN:
            if my_event.key == pygame.K_LEFT:
                self.move_right = True
            if my_event.key == pygame.K_RIGHT:
                self.move_left = True
            if my_event.key == pygame.K_UP:
                self.move_up = True
            if my_event.key == pygame.K_DOWN:
                self.move_down = True

        if my_event.type == pygame.KEYUP:
            if my_event.key == pygame.K_LEFT:
                self.move_right = False
            if my_event.key == pygame.K_RIGHT:
                self.move_left = False
            if my_event.key == pygame.K_UP:
                self.move_up = False
            if my_event.key == pygame.K_DOWN:
                self.move_down = False
        # cheat
        if my_event.type == pygame.MOUSEBUTTONDOWN:
            if Player.cheat:
                self.position_x, self.position_y = event.pos

    def draw(self):
        screen.blit(self.image, (self.position_x, self.position_y))


class Meteor:
    meteor_set = set()
    count = 0
    max_speed_meteor = 5
    max_meteor_size = 50

    def __init__(self, position_x=None, position_y=None, size=None):
        global MAX_X
        global MAX_Y

        if size is None:
            size = random.randint(15, Meteor.max_meteor_size)
        if position_x is None:
            position_x = random.randint(MAX_X // 8 * 7, MAX_X + 4 * size)
        if position_y is None:
            position_y = random.randint(size + random.randint(0, 20), MAX_Y - size - random.randint(0, 20))

        self.position_x = position_x
        self.position_y = position_y
        self.size = size
        self.speed = - random.randint(2, Meteor.max_speed_meteor)

        self.image = pygame.image.load(path.join(DIR_ALL, f'asteroid{random.randint(1, 3)}.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (size, size))

        Meteor.meteor_set.add(self)

    def create(self):
        Meteor.count += 1
        screen.blit(self.image, (self.position_x, self.position_y))

    def move(self):
        self.position_x += self.speed
        self.position_y += self.speed // 2 * random.randint(-1, 1)

    def remove(self):
        Meteor.count -= 1
        Meteor.meteor_set.remove(self)

    def draw(self):
        screen.blit(self.image, (self.position_x, self.position_y))

    def crash(self):
        random.choice(exp_sound).play()
        self.size += 1


# _____________Point functions______________
def create_all_point():
    new_point = Point()
    new_point.create()


def draw_all_point():
    for local_point in Point.point_set:
        local_point.draw()


def find_and_remove_point(x_now, y_now):
    global SIZE_X
    global SIZE_Y

    array_eat_point = []
    for version in Point.point_set:
        remove_x = False
        remove_y = False

        if x_now + SIZE_X >= version.position_x + version.size:
            if x_now <= version.position_x:
                remove_x = True
        if y_now + SIZE_Y >= version.position_y + version.size:
            if y_now <= version.position_y:
                remove_y = True

        if remove_x is True and remove_y is True:
            array_eat_point.append(version)
            random.choice(coin_sound_all).play()

    for point in array_eat_point:
        point.remove()


def create_meteor():
    new_meteor = Meteor()
    new_meteor.create()


# _______________Meteor functions____________
def create_cluster_meteor(max_count_meteor):
    count_meteor = random.randint(4, max_count_meteor)
    for i in range(count_meteor):
        create_meteor()


# move and remove
def move_meteor():
    for version_meteor in Meteor.meteor_set:
        version_meteor.move()

    array_not_show_meteor = []
    for version_meteor in Meteor.meteor_set:
        if version_meteor.position_x < -version_meteor.size:
            array_not_show_meteor.append(version_meteor)

    for version_meteor in array_not_show_meteor:
        version_meteor.remove()
        del version_meteor


def draw_meteor():
    for version_meteor in Meteor.meteor_set:
        version_meteor.draw()


# find crash
def crash_player_and_meteor(position_x, position_y):
    global SIZE_X
    global SIZE_Y
    global game_over

    crash = False
    for version_meteor in Meteor.meteor_set:
        if position_y + SIZE_Y + version_meteor.size >= version_meteor.position_y + version_meteor.size >= position_y:
            if position_x + SIZE_X >= version_meteor.position_x >= position_x + SIZE_X - Meteor.max_speed_meteor:
                crash = True
            if position_x + Meteor.max_speed_meteor >= version_meteor.position_x + version_meteor.size >= position_x:
                crash = True
        if position_x + SIZE_X + version_meteor.size >= version_meteor.position_x + version_meteor.size >= position_x:
            if position_y + SIZE_Y >= version_meteor.position_y >= position_y + SIZE_Y - Meteor.max_speed_meteor:
                crash = True
            if position_y + Meteor.max_speed_meteor >= version_meteor.position_y + version_meteor.size >= position_y:
                crash = True
        if crash:
            version_meteor.crash()
            break

    if crash:
        game_over = True


# _______________Person function______________
# generation array
def create_array_person(x):
    global SIZE_X_SHOW
    global SIZE_Y_SHOW

    image = f'player{x}.png'
    image = path.join(DIR_ALL, image)
    image = pygame.image.load(image).convert_alpha()
    image = pygame.transform.scale(image, (SIZE_X_SHOW, SIZE_Y_SHOW))
    return image


def find_three_person(array):
    global index_for_start_top_three
    global array_persons_locked
    dop = array_persons_locked[index_for_start_top_three: index_for_start_top_three + 3]
    return array[index_for_start_top_three:index_for_start_top_three + 3], dop


def move_person(my_event):
    global index_for_start_top_three
    global array_persons

    if my_event.type == pygame.KEYDOWN:
        if my_event.key == pygame.K_LEFT:
            index_for_start_top_three -= 1
            swipe.play()
        elif my_event.key == pygame.K_RIGHT:
            index_for_start_top_three += 1
            swipe.play()

    if index_for_start_top_three < 0:
        index_for_start_top_three = 0
    if index_for_start_top_three > len(array_persons) - 3:
        index_for_start_top_three = len(array_persons) - 3


# _____________Name play_____________
def name_and_rule():
    img_dir = path.join(path.dirname(__file__), 'name_game')
    break_name = False
    for index_name in range(9):
        back_ground_local = pygame.image.load(path.join(img_dir, f'name{index_name}.png')).convert()
        back_ground_local = pygame.transform.scale(back_ground_local, (MAX_X, MAX_Y))
        screen.blit(back_ground_local, (0, 0))
        pygame.display.flip()
        for event_rule in pygame.event.get():
            if event_rule.type == pygame.KEYDOWN:
                if event_rule.key == pygame.K_RETURN:
                    break_name = True
                elif event_rule.key == pygame.K_ESCAPE:
                    end_global()
        sleep(0.3)
        if break_name:
            break
    sleep(0.2)

    language = ['en', 'ru']
    i_lan = 0
    continue_game = False
    img_dir_rules = path.join(path.dirname(__file__), 'rules')
    while continue_game is False:
        for event_rule in pygame.event.get():
            if event_rule.type == pygame.KEYDOWN:
                if event_rule.key == pygame.K_RETURN:
                    continue_game = True
                elif event_rule.key == pygame.K_ESCAPE:
                    end_global()
            elif event_rule.type == pygame.MOUSEBUTTONDOWN:
                x_mouse, y_mouse = event_rule.pos
                if 955 <= x_mouse <= 999 and 16 <= y_mouse <= 52:
                    i_lan = (i_lan + 1) % 2

        back_ground_local = pygame.image.load(path.join(img_dir_rules, f'rule2_{language[i_lan]}.png')).convert()
        back_ground_local = pygame.transform.scale(back_ground_local, (MAX_X, MAX_Y))
        screen.blit(back_ground_local, (0, 0))
        pygame.display.flip()


# ____________Setting________________
def setting():
    def draw_user_text(nick):
        global cursor

        nick += cursor

        f_user_text = pygame.font.SysFont(FONT_GLOBAL, 39)
        user_text = f_user_text.render(nick, 0, (0, 0, 0))
        screen.blit(user_text, (MAX_X - MAX_X // 10 - 300 - 100, 57))

    def draw_three_person():
        three_person, three_locked = find_three_person(array_persons)
        i = 0
        for person in three_person:
            if person is not None:
                screen.blit(person, array_persons_positions[i])
                if three_locked[i][1] is not None and three_locked[i][0] > Player.score_max:
                    screen.blit(three_locked[i][1], array_persons_positions[i])
            i += 1

    global SIZE_X_SHOW
    global SIZE_Y_SHOW
    global FONT_GLOBAL
    global FONT_GLOBAL_BASIS
    global COLOR_GLOBAL
    global nickname
    global array_persons_positions
    global array_persons
    global array_persons_locked
    arr = array_persons_locked

    # object for setting
    global game_start

    color_nickname = (150, 250, 250)
    different_position_frame_and_person = 50

    # frame
    frame_person_position = (387 - different_position_frame_and_person, 190 - different_position_frame_and_person)
    frame_person_image = path.join(DIR_ALL, 'frame.png')
    frame_person_image = pygame.image.load(frame_person_image).convert_alpha()
    frame_person_image = pygame.transform.scale(frame_person_image,
                                                (SIZE_X_SHOW + 2 * different_position_frame_and_person,
                                                 SIZE_Y_SHOW + 2 * different_position_frame_and_person))

    # text fon
    text_position = (MAX_X // 10 + 300, MAX_Y // 12 - 0)
    text_image = path.join(DIR_ALL, 'text3.png')
    text_image = pygame.image.load(text_image).convert_alpha()
    text_image = pygame.transform.scale(text_image, (MAX_X - MAX_X // 10 - 300 - 100, 60))

    while game_start is False:
        screen.blit(back_ground, (0, 0))

        # nickname
        f3 = pygame.font.SysFont(FONT_GLOBAL, 56)
        text_start = f3.render('Nickname:', 1, color_nickname)
        screen.blit(text_start, (MAX_X // 10, MAX_Y // 12))
        # person move
        for start_event in pygame.event.get():
            if start_event.type == pygame.KEYDOWN:
                if start_event.key == pygame.K_RETURN:
                    ind = index_for_start_top_three
                    bool_start = True
                    if arr[ind + 1][1] is not None and arr[ind + 1][0] > Player.score_max:
                        bool_start = False
                    if bool_start:
                        game_start = True
                elif start_event.key == 8:  # backspace
                    nickname = nickname[: - 1]
                elif start_event.key == 32:  # space
                    pass
                elif start_event.key == pygame.K_ESCAPE:
                    end_global()
                else:
                    if len(nickname) < 10:
                        nickname += start_event.unicode
            move_person(start_event)

        draw_three_person()
        screen.blit(frame_person_image, frame_person_position)
        screen.blit(text_image, text_position)
        draw_user_text(nickname)

        f = pygame.font.SysFont(FONT_GLOBAL_BASIS, 56)

        if array_persons_locked[index_for_start_top_three + 1][0] > Player.score_max:
            score_locked = f.render(f'Score:{array_persons_locked[index_for_start_top_three + 1][0]}', 1, COLOR_GLOBAL)
            screen.blit(score_locked, (390, 450))

        f_game_over = pygame.font.SysFont(FONT_GLOBAL, 20)
        score_end = f_game_over.render(f'Please click enter to complete', 1, (150, 230, 230))
        screen.blit(score_end, (MAX_X // 2 - 145, MAX_Y - 35))

        pygame.display.flip()

    if game_start:
        player.image = array_persons[index_for_start_top_three + 1]
        if index_for_start_top_three + 3 == len(array_persons):
            Player.cheat = True
        player.image = pygame.transform.scale(player.image, (SIZE_X, SIZE_Y))

    sleep(0.1)


# _____________Start___________________
def start():
    global MAX_X
    global MAX_Y
    global FONT_GLOBAL_BASIS
    global COLOR_GLOBAL

    screen.blit(back_ground, (0, 0))
    f_go_to = pygame.font.SysFont(FONT_GLOBAL_BASIS, 136)
    text_go_to = f_go_to.render('Go to play!', 1, COLOR_GLOBAL)
    screen.blit(text_go_to, (MAX_X // 2 - 300, MAX_Y // 2 - 130))
    pygame.display.flip()
    sleep(1)


# ____________Pause___________________
def pause():
    global FONT_GLOBAL_BASIS
    global COLOR_GLOBAL

    pause_sound.play()

    player.move_right = False
    player.move_left = False
    player.move_up = False
    player.move_down = False

    game_pause_bool = True
    f = pygame.font.SysFont(FONT_GLOBAL_BASIS, 136)
    game_end = f.render('Pause!', 1, COLOR_GLOBAL)
    screen.blit(game_end, (MAX_X // 2 - 200, MAX_Y // 2 - 110))
    pygame.display.flip()
    while game_pause_bool:
        for event_in_pause in pygame.event.get():
            if event_in_pause.type == pygame.KEYDOWN:
                if event_in_pause.key == pygame.K_SPACE:
                    game_pause_bool = False
                elif event_in_pause.key == pygame.K_ESCAPE:
                    end_global()
            player.event_player(event)


# ____________Finish__________________
def finish():
    global MAX_X
    global MAX_Y
    global FONT_GLOBAL_BASIS
    global FONT_GLOBAL
    global COLOR_GLOBAL

    f_game_over = pygame.font.SysFont(FONT_GLOBAL_BASIS, 136)
    text_game_over = f_game_over.render('Game over!', 1, COLOR_GLOBAL)
    screen.blit(text_game_over, (MAX_X // 2 - 300, MAX_Y // 2 - 130))
    pygame.display.flip()
    sleep(3)
    screen.blit(back_ground, (0, 0))
    screen.blit(text_game_over, (MAX_X // 2 - 300, MAX_Y // 2 - 130))
    f_game_over = pygame.font.SysFont(FONT_GLOBAL, 40)
    score_end = f_game_over.render(f'Score: {Point.score}', 1, (150, 230, 230))
    screen.blit(score_end, (MAX_X // 2 - 95, MAX_Y - 50))
    pygame.display.flip()
    sleep(3)


# ____________Rating_________________
def rating():
    global nickname
    global FONT_GLOBAL
    global MAX_X
    global MAX_Y

    def create_mini_array(x):
        return list(x.split())

    def sort_rating(array):
        for i_for_sort in range(len(array) - 1, 0, -1):
            if int(array[i_for_sort][1]) > int(array[i_for_sort - 1][1]):
                array[i_for_sort], array[i_for_sort - 1] = array[i_for_sort - 1], array[i_for_sort]
        return array

    def draw_rating_all(array_rating_local):
        global FONT_GLOBAL_BASIS
        # global FONT_GLOBAL
        global COLOR_GLOBAL

        # global MAX_X
        # global MAX_Y
        # global nickname

        def function_for_place(x):
            return f'{x} place'

        array_rating_local.append([nickname, Point.score])
        array = ['The Grand prix', *(map(function_for_place, range(1, 4))), 'You score']

        def draw_rating_name(font_basis, color, max_x, max_y):
            f_rating_name = pygame.font.SysFont(font_basis, 96)
            text_go_to = f_rating_name.render('Rating', 1, color)
            screen.blit(text_go_to, (max_x // 2 - 140, max_y // 11 - 80))

        def draw_name_top(font, text, diff, diff_x=0, color=(150, 250, 250)):
            f_name_to = pygame.font.SysFont(font, 50)
            text_name = f_name_to.render(text, 1, color)
            screen.blit(text_name, (MAX_X // 5 - 120 + diff_x, MAX_Y // 10 + 50 + diff))

        draw_rating_name(FONT_GLOBAL_BASIS, COLOR_GLOBAL, MAX_X, MAX_Y)
        dif = 80
        for index in range(len(array)):
            draw_name_top(FONT_GLOBAL, array[index], dif * index, - 20)
            text_nem_and_score = f'{array_rating_local[index][0]}'
            draw_name_top(FONT_GLOBAL, text_nem_and_score, dif * index, 410, color=(250, 57, 98))
            text_nem_and_score = f'{array_rating_local[index][1]}'
            draw_name_top(FONT_GLOBAL, text_nem_and_score, dif * index, 700)
            if index is 3:
                dif += 9

    with open('rating_user.txt', 'r') as f:
        array_rating = list(map(create_mini_array, f.read().split('\n')))
        Player.score_record = int(array_rating[0][1])
        if nickname in ('', ' ', '  '):
            nickname = '_'
        array_rating.append(list((nickname, Point.score)))
        array_rating = sort_rating(array_rating)

    with open('rating_user.txt', 'w') as f:
        for i in range(len(array_rating)):
            mini_array = array_rating[i]
            if i < 3:
                f.write(f'{mini_array[0]} {mini_array[1]}\n')
            elif i == 3:
                f.write(f'{mini_array[0]} {mini_array[1]}')

    rating_end = False
    while rating_end is False:
        # draw back ground
        screen.blit(back_ground, (0, 0))
        draw_rating_all(array_rating[:4])

        for event_rating in pygame.event.get():
            if event_rating.type == pygame.KEYDOWN:
                if event_rating.key == pygame.K_RETURN:
                    rating_end = True
                elif event_rating.key == pygame.K_ESCAPE:
                    end_global()

        f_game_over = pygame.font.SysFont(FONT_GLOBAL, 20)
        score_end = f_game_over.render(f'Please click enter to complete', 1, (150, 230, 230))
        screen.blit(score_end, (MAX_X // 2 - 145, MAX_Y - 35))

        pygame.display.flip()
        clock.tick(fps)


# ____________THE END________________
def end_global(no_end=False):
    time_end = 0
    end = False
    while time_end < 10 ** 4 and end is False:
        time_end += 1
        screen.blit(back_ground, (0, 0))

        f = pygame.font.SysFont(FONT_GLOBAL_BASIS, 136)
        game_end = f.render('Thanks!', 1, COLOR_GLOBAL)
        screen.blit(game_end, (MAX_X // 2 - 200, MAX_Y // 2 - 110))

        f_game_over = pygame.font.SysFont(FONT_GLOBAL, 20)
        score_end = f_game_over.render(f'Please click enter to complete', 1, (150, 230, 230))
        screen.blit(score_end, (MAX_X // 2 - 145, MAX_Y - 35))

        for event_end in pygame.event.get():
            if event_end.type == pygame.KEYDOWN:
                if event_end.key == pygame.K_RETURN:
                    end = True

        pygame.display.flip()
        clock.tick(fps)
    if no_end is not True:
        sys.exit()


# ______________Reward________________
def reward():
    def crash_record():
        img_dir = path.join(path.dirname(__file__), 'win')
        break_name = False
        for index_name in range(-1, 18):
            back_ground_local = pygame.image.load(path.join(img_dir, f'win{index_name}.png')).convert()
            back_ground_local = pygame.transform.scale(back_ground_local, (MAX_X, MAX_Y))
            screen.blit(back_ground_local, (0, 0))
            pygame.display.flip()
            for event_rule in pygame.event.get():
                if event_rule.type == pygame.KEYDOWN:
                    if event_rule.key == pygame.K_RETURN:
                        break_name = True
                    elif event_rule.key == pygame.K_ESCAPE:
                        end_global()
            sleep(0.25)
            if break_name:
                break
        sleep(0.1)

        language = ['en', 'ru']
        i_lan = 0
        continue_game = False
        img_dir_rules = img_dir
        while continue_game is False:
            for event_rule in pygame.event.get():
                if event_rule.type == pygame.KEYDOWN:
                    if event_rule.key == pygame.K_RETURN:
                        continue_game = True
                    elif event_rule.key == pygame.K_ESCAPE:
                        end_global()
                elif event_rule.type == pygame.MOUSEBUTTONDOWN:
                    x_mouse, y_mouse = event_rule.pos
                    if 955 <= x_mouse <= 999 and 16 <= y_mouse <= 52:
                        i_lan = (i_lan + 1) % 2

            back_ground_local = pygame.image.load(path.join(img_dir_rules, f'win_{language[i_lan]}.png')).convert()
            back_ground_local = pygame.transform.scale(back_ground_local, (MAX_X, MAX_Y))
            screen.blit(back_ground_local, (0, 0))
            pygame.display.flip()

    if Point.score >= Player.score_record:
        crash_record()


# initialization constants
DIR_ALL = path.join(path.dirname(__file__), 'all_file')
MAX_X = 1024
MAX_Y = 576
MAX_SHOW = 35
SIZE_X = 100
SIZE_Y = 100
SIZE_X_SHOW = 250
SIZE_Y_SHOW = 250
FONT_GLOBAL = 'simsunnsimsun'
COLOR_GLOBAL = (250, 57, 138)
FONT_GLOBAL_BASIS = 'curlz'

# initialization names
max_show_meteor = 7
game_over = False
game_pause = False
my_time = 0
fps = 45
flag_time_for_meteor = 0
nickname = ''
cursor = '|'

# initialization py.game's objects
pygame.init()
screen = pygame.display.set_mode((MAX_X, MAX_Y))
pygame.display.set_caption('CosmoDrone game')
clock = pygame.time.Clock()
back_ground = pygame.transform.scale(pygame.image.load('cosmos.png').convert(), (MAX_X, MAX_Y))

#    back_ground = pygame.transform.scale(pygame.image.load(path.join(DIR_ALL, 'cosmos.png')).convert(), (MAX_X, MAX_Y))

screen.blit(back_ground, (0, 0))
pygame.display.flip()

# size and style text score, but no color
f1 = pygame.font.Font(None, 36)

# for setting
array_persons_positions = [(68, 230), (387, 190), (706, 230)]
array_persons = [None] + list(map(create_array_person, range(7))) + [None]
locked = 'locked.png'
locked = path.join(DIR_ALL, locked)
locked = pygame.image.load(locked).convert_alpha()
locked = pygame.transform.scale(locked, (SIZE_X_SHOW, SIZE_Y_SHOW))
array_persons_locked = [[0, None]] * (len(array_persons) - 6) + list(([100, locked], [250, locked], [500, locked],
                                                                      [1000, locked], [4900, locked])) + [[0, None]]
game_start = False
index_for_start_top_three = 1

# sound in game
snd_dir = path.join(path.dirname(__file__), 'sound')
swipe = pygame.mixer.Sound(path.join(snd_dir, 'Blip_Select.wav'))
swipe.set_volume(0.2)
pause_sound = pygame.mixer.Sound(path.join(snd_dir, 'Decline.wav'))
pause_sound.set_volume(0.5)
coin_sound_all = []
for coin in range(1, 11):
    coin_sound = pygame.mixer.Sound(path.join(snd_dir, f'coin{coin}.wav'))
    coin_sound.set_volume(0.5)
    coin_sound_all.append(coin_sound)
coin_sound = pygame.mixer.Sound(path.join(snd_dir, 'Coin.wav'))
coin_sound.set_volume(0.5)
coin_sound_all.append(coin_sound)
exp_sound = []
for snd in ['Exp1.wav', 'Exp2.wav']:
    exp_sound.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
exp_sound[0].set_volume(0.3)
exp_sound[1].set_volume(0.2)

# create object Player
player = Player()

# _________________Name play_____________
name_and_rule()

# _________________Setting_______________
setting()

# _________________Start_________________
start()

# _________________Game__________________
while game_over is False:
    # draw back ground
    screen.blit(back_ground, (0, 0))

    # event players decoder
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause()
            elif event.key == pygame.K_ESCAPE:
                end_global()

        player.event_player(event)

    # create point
    if Point.count < MAX_SHOW and my_time % random.randint(15, 60) == 0:
        create_all_point()
        if my_time > 10 ** 4:
            my_time = 0

    # create cluster
    if Point.score % 300 == 0 and my_time - flag_time_for_meteor > 100 or my_time % 1000 == 0 and my_time > 100:
        create_cluster_meteor(max_show_meteor)
        flag_time_for_meteor = my_time
        max_show_meteor += 1

    # find crash with meteor
    if Meteor.count > 0:
        crash_player_and_meteor(player.position_x, player.position_y)

    # move all  meteors
    move_meteor()
    # monster motion
    player.motion_player()
    # eat point
    find_and_remove_point(player.position_x, player.position_y)

    # players score
    score = f1.render(f'Score {Point.score}', 1, (150, 250, 250))

    # draw player, point and score and meteor
    draw_all_point()
    player.draw()
    draw_meteor()
    screen.blit(score, (MAX_X - 160, MAX_Y - 40))

    pygame.display.flip()
    clock.tick(fps)

    my_time += 1

# _________________Finish_________________
finish()
sleep(1)

# _________________Rating________________
rating()

# _________________THE END_______________
end_global(no_end=True)

# __________________Reward_______________
reward()
