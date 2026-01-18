import arcade
import math
import random
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_WIDTH_GAME = 1000
SCREEN_HEIGHT_GAME = 650
SCREEN_TITLE = "GameStart"
SECOND_WINDOW_TITLE = "Game"
DIFFICULTY_LEVEL = 0
player = 0
WINNER = ""
SCORE = []


# ======= Класс для первого окна ======
class WelcomeView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        # текстовый обьект
        self.text_object = arcade.Text(
            "",
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2 + 15,
            color=arcade.color.YELLOW_ROSE,
            font_size=100,
            font_name="Impact",
            anchor_x="center",
            anchor_y="center",
            bold=False
        )
        self.time_elapsed = 0

        # параметры пульсации стартовой кнопки
        self.start_base_scale = 0.3
        self.pulse_amplitude = 0.02
        self.pulse_speed = 8

        self.ball_rotation_speed = 300

        # создание списка спрайтов
        self.all_sprites = arcade.SpriteList()

        # создание спрайтов
        self.tennisist_sprite_1 = arcade.Sprite("pictures/tennisist.png", scale=0.35)
        self.tennisist_sprite_1.center_x = SCREEN_WIDTH // 3
        self.tennisist_sprite_1.center_y = 300
        self.all_sprites.append(self.tennisist_sprite_1)

        self.tennisist_sprite_2 = arcade.Sprite("pictures/tenn3.png", scale=0.2)
        self.tennisist_sprite_2.center_x = SCREEN_WIDTH - 150
        self.tennisist_sprite_2.center_y = 100
        self.all_sprites.append(self.tennisist_sprite_2)

        self.start_sprite = arcade.Sprite("pictures/startbutton.png", scale=0.3)
        self.start_sprite.center_x = SCREEN_WIDTH // 2
        self.start_sprite.center_y = SCREEN_HEIGHT // 2 - 140
        self.all_sprites.append(self.start_sprite)

        self.setup_sprite = arcade.Sprite("pictures/setup.png", scale=0.10)
        self.setup_sprite.center_x = 40
        self.setup_sprite.center_y = SCREEN_HEIGHT - 40
        self.all_sprites.append(self.setup_sprite)

        self.tennball = arcade.Sprite("pictures/tennball.png", scale=0.15)
        self.tennball.center_x = SCREEN_WIDTH - 120
        self.tennball.center_y = SCREEN_HEIGHT - 120
        self.all_sprites.append(self.tennball)

        global SCORE
        if os.path.exists("score.txt"):
            with open("score.txt", "r", encoding="utf-8-sig") as f:
                k = f.readlines()
                for score in k:
                    SCORE.append(int(score.rstrip()))
        else:
            with open("score.txt", "w", encoding="utf-8-sig") as f:
                f.write("0\n")
                f.write("0")
            with open("score.txt", "r", encoding="utf-8-sig") as f:
                k = f.readlines()
                for score in k:
                    SCORE.append(int(score.rstrip()))

        self.score = arcade.Text(
            f"{SCORE[0]} : {SCORE[1]}",
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2 + 150,
            color=arcade.color.YELLOW_ROSE,
            font_size=85,
            font_name="Impact",
            anchor_x="center",
            anchor_y="center",
            bold=False
        )

    def on_update(self, delta_time):
        # обновление времени
        self.time_elapsed += delta_time

        # формула для пульсации стартовой кнопки
        pulse_scale = self.start_base_scale + self.pulse_amplitude * math.sin(self.pulse_speed * self.time_elapsed)
        self.start_sprite.scale = pulse_scale

        # расчет угла вращение мяча
        self.tennball.angle += self.ball_rotation_speed * delta_time
        if self.tennball.angle >= 360:
            self.tennball.angle -= 360
        elif self.tennball.angle < 0:
            self.tennball.angle += 360

    def on_draw(self):
        self.clear()
        # отрисовка всех спрайтов
        self.all_sprites.draw()

        # отрисовка текста
        self.text_object.value = "PONG"
        self.text_object.draw()
        self.score.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        # проверка нажатия на стартовую кнопку
        if self.start_sprite.collides_with_point((x, y)):
            # открытие второго окна
            game_view = SecondView()
            self.window.show_view(game_view)
        elif self.setup_sprite.collides_with_point((x, y)):
            game_view = SetupView()
            self.window.show_view(game_view)


# ====== Класс для 2 окна =======
class SecondView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        # параметры пульсации текста
        self.time_elapsed = 0
        self.pulse_speed = 7
        self.pulse_min_scale = 0.9
        self.pulse_max_scale = 1.1

        # текстовые обьекты
        self.choose_text = arcade.Text(
            "",
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2 + 200,
            color=arcade.color.YELLOW_ROSE,
            font_size=50,
            font_name="Impact",
            anchor_x="center",
            anchor_y="center",
            bold=False
        )

        self.easy_text = arcade.Text(
            "",
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2 + 100,
            color=arcade.color.YELLOW_ROSE,
            font_size=30,
            font_name="Impact",
            anchor_x="center",
            anchor_y="center",
            bold=False
        )

        self.medium_text = arcade.Text(
            "",
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2,
            color=arcade.color.YELLOW_ROSE,
            font_size=30,
            font_name="Impact",
            anchor_x="center",
            anchor_y="center",
            bold=False
        )

        self.hard_text = arcade.Text(
            "",
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2 - 100,
            color=arcade.color.YELLOW_ROSE,
            font_size=30,
            font_name="Impact",
            anchor_x="center",
            anchor_y="center",
            bold=False
        )

        self.back_text = arcade.Text(
            "",
            x=100,
            y=SCREEN_HEIGHT // 2 - 200,
            color=arcade.color.YELLOW_ROSE,
            font_size=30,
            font_name="Impact",
            anchor_x="center",
            anchor_y="center",
            bold=False
        )

        self.insane_text = arcade.Text("",
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2 - 200,
            color=arcade.color.YELLOW_ROSE,
            font_size=30,
            font_name="Impact",
            anchor_x="center",
            anchor_y="center",
            bold=False)

        # создание списка спрайтов
        self.all_sprites = arcade.SpriteList()

        # создание кнопок-спрайтов
        self.botton_sprite_1 = arcade.Sprite("pictures/botton.png", scale=0.5)
        self.botton_sprite_1.center_x = SCREEN_WIDTH // 2
        self.botton_sprite_1.center_y = SCREEN_HEIGHT // 2 - 2.5 + 100
        self.all_sprites.append(self.botton_sprite_1)

        self.botton_sprite_2 = arcade.Sprite("pictures/botton.png", scale=0.5)
        self.botton_sprite_2.center_x = SCREEN_WIDTH // 2
        self.botton_sprite_2.center_y = SCREEN_HEIGHT // 2 - 102.5 + 100
        self.all_sprites.append(self.botton_sprite_2)

        self.botton_sprite_3 = arcade.Sprite("pictures/botton.png", scale=0.5)
        self.botton_sprite_3.center_x = SCREEN_WIDTH // 2
        self.botton_sprite_3.center_y = SCREEN_HEIGHT // 2 - 202.5 + 100
        self.all_sprites.append(self.botton_sprite_3)

        self.botton_sprite_4 = arcade.Sprite("pictures/botton.png", scale=0.5)
        self.botton_sprite_4.center_x = 100
        self.botton_sprite_4.center_y = SCREEN_HEIGHT // 2 - 202.5
        self.all_sprites.append(self.botton_sprite_4)

        self.botton_sprite_5 = arcade.Sprite("pictures/botton.png", scale=0.5)
        self.botton_sprite_5.center_x = SCREEN_WIDTH // 2
        self.botton_sprite_5.center_y = SCREEN_HEIGHT // 2 - 202.5
        self.all_sprites.append(self.botton_sprite_5)

    def on_update(self, delta_time):
        # обновление времени
        self.time_elapsed += delta_time

    def on_draw(self):
        self.clear()

        # значения текстовых обьектов
        self.choose_text.value = "CHOOSE DIFFICULTY"
        self.easy_text.value = "EASY"
        self.medium_text.value = "MEDIUM"
        self.hard_text.value = "HARD"
        self.back_text.value = "BACK"
        self.insane_text.value = "INSANE"

        # формула для пульсации текста
        pulse_factor = (math.sin(self.time_elapsed * self.pulse_speed) + 1) / 2  # от 0 до 1
        current_scale = self.pulse_min_scale + (self.pulse_max_scale - self.pulse_min_scale) * pulse_factor

        # значальный размер шрифта
        original_font_size = 50

        # обновление текста (для пульсации)
        pulsating_text = arcade.Text(
            "CHOOSE DIFFICULTY",
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2 + 200,
            color=arcade.color.YELLOW_ROSE,
            font_size=int(original_font_size * current_scale),
            font_name="Impact",
            anchor_x="center",
            anchor_y="center",
            bold=False
        )

        # отрисовка пульсирующего текста
        pulsating_text.draw()

        self.all_sprites.draw()

        # отрисовка текста кнопок
        self.easy_text.draw()
        self.medium_text.draw()
        self.hard_text.draw()
        self.back_text.draw()
        self.insane_text.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        global DIFFICULTY_LEVEL
        # проверка нажатия на кнопку сложности
        if self.botton_sprite_1.collides_with_point((x, y)):
            DIFFICULTY_LEVEL = 1
            game_view = GameWindow()
            self.window.show_view(game_view)
        elif self.botton_sprite_2.collides_with_point((x, y)):
            DIFFICULTY_LEVEL = 2
            game_view = GameWindow()
            self.window.show_view(game_view)
        elif self.botton_sprite_3.collides_with_point((x, y)):
            DIFFICULTY_LEVEL = 3
            game_view = GameWindow()
            self.window.show_view(game_view)
        elif self.botton_sprite_4.collides_with_point((x, y)):
            game_view = WelcomeView()
            self.window.show_view(game_view)
        elif self.botton_sprite_5.collides_with_point((x, y)):
            DIFFICULTY_LEVEL = 4
            game_view = GameWindow()
            self.window.show_view(game_view)

    def on_show_view(self):
        self.window.set_size(SCREEN_WIDTH, SCREEN_HEIGHT)


# ===== Класс для легкой игры =======
class GameWindow(arcade.View):
    player = 1
    def __init__(self):
        super().__init__()
        self.count_1 = 0
        self.count_2 = 0
        arcade.set_background_color(arcade.color.BLACK)


        self.all_sprites = arcade.SpriteList()

        global DIFFICULTY_LEVEL

        if DIFFICULTY_LEVEL == 1:
            self.texture = arcade.load_texture("pictures/cort.jfif")
        if DIFFICULTY_LEVEL == 2:
            self.texture = arcade.load_texture("pictures/city.jpg")
        if DIFFICULTY_LEVEL == 3:
            self.texture = arcade.load_texture("pictures/apocal.jpg")
        if DIFFICULTY_LEVEL == 4:
            self.texture = arcade.load_texture("pictures/newspace.png")


        self.player1_speed = 450
        self.player_speed = 450

        self.hero_1_x = SCREEN_WIDTH_GAME - 960
        self.hero_1_y = SCREEN_HEIGHT_GAME // 2

        self.hero_2_x = SCREEN_WIDTH_GAME - 40
        self.hero_2_y = SCREEN_HEIGHT_GAME // 2

        self.keys_pressed = set()
        self.player_1_textures = []
        self.player_2_textures = []
        for k in range(8):
            if DIFFICULTY_LEVEL == 1:
                texture = arcade.load_texture(
                    f":resources:images/animated_characters/female_person/femalePerson_walk{k}.png"
                )
            elif DIFFICULTY_LEVEL == 2:
                texture = arcade.load_texture(
                    f":resources:images/animated_characters/female_adventurer/femaleAdventurer_walk{k}.png"
                )
            elif DIFFICULTY_LEVEL == 3:
                texture = arcade.load_texture(
                    f":resources:images/animated_characters/female_adventurer/femaleAdventurer_walk{k}.png"
                )
            elif DIFFICULTY_LEVEL == 4:
                texture = arcade.load_texture(
                    f":resources:images/animated_characters/robot/robot_walk{k}.png"
                                              )
            self.player_1_textures.append(texture)
        for i in range(8):
            if DIFFICULTY_LEVEL == 1:
                texture = arcade.load_texture(
                    f":resources:images/animated_characters/male_person/malePerson_walk{i}.png"
                )
            elif DIFFICULTY_LEVEL == 2:
                texture = arcade.load_texture(
                    f":resources:images/animated_characters/male_adventurer/maleAdventurer_walk{i}.png"
                )
            elif DIFFICULTY_LEVEL == 3:
                texture = arcade.load_texture(
                    f":resources:images/animated_characters/zombie/zombie_walk{i}.png"
                )
            elif DIFFICULTY_LEVEL == 4:
                texture = arcade.load_texture(
                    f":resources:images/animated_characters/robot/robot_walk{i}.png"
                )
            self.player_2_textures.append(texture)

        self.player_sprite_1 = arcade.Sprite()
        self.player_sprite_1.texture = self.player_1_textures[0]
        self.player_sprite_1.center_x = self.hero_1_x
        self.player_sprite_1.center_y = self.hero_1_y
        # Задаем размеры для спрайта игрока 1
        self.player_sprite_1.width = 70
        self.player_sprite_1.height = 100
        self.all_sprites.append(self.player_sprite_1)

        self.player_sprite_2 = arcade.Sprite()
        self.player_sprite_2.texture = self.player_2_textures[0]
        self.player_sprite_2.center_x = self.hero_2_x
        self.player_sprite_2.center_y = self.hero_2_y
        # Задаем размеры для спрайта игрока 2
        self.player_sprite_2.width = 70
        self.player_sprite_2.height = 100
        self.all_sprites.append(self.player_sprite_2)

        self.current_texture_1 = 0
        self.time_since_last_frame_1 = 0
        self.frame_duration_1 = 0.1

        self.current_texture_2 = 0
        self.time_since_last_frame_2 = 0
        self.frame_duration_2 = 0.1

        self.wall_list = arcade.SpriteList()
        # Нижние стены
        for x in range(0, SCREEN_WIDTH_GAME, 64):
            if DIFFICULTY_LEVEL == 1:
                wall = arcade.Sprite(":resources:images/tiles/grassMid.png", 0.4)
            elif DIFFICULTY_LEVEL == 2:
                wall = arcade.Sprite(":resources:images/tiles/stoneMid.png", 0.4)
            elif DIFFICULTY_LEVEL == 3:
                wall = arcade.Sprite(":resources:images/tiles/lavaTop_low.png", 0.4)
            elif DIFFICULTY_LEVEL == 4:
                wall = arcade.Sprite(":resources:images/tiles/planetMid.png", 0.4)
            wall.center_x = x
            wall.center_y = 32
            wall.width = 64
            wall.height = 64
            self.wall_list.append(wall)

        # Верхние стены
        for x in range(0, SCREEN_WIDTH_GAME, 64):
            if DIFFICULTY_LEVEL == 1:
                wall = arcade.Sprite(":resources:images/tiles/water.png", 0.4)
            elif DIFFICULTY_LEVEL == 2:
                wall = arcade.Sprite(":resources:images/tiles/snowCenter.png", 0.4)
            elif DIFFICULTY_LEVEL == 3:
                wall = arcade.Sprite(":resources:images/tiles/planetCenter.png", 0.4)
            elif DIFFICULTY_LEVEL == 4:
                wall = arcade.Sprite(":resources:images/tiles/planetCenter.png", 0.4)

            wall.center_x = x
            wall.center_y = SCREEN_HEIGHT_GAME - 32  # Правильная высота
            wall.width = 64
            wall.height = 64
            self.wall_list.append(wall)

        #мячик
        if DIFFICULTY_LEVEL == 1:
            self.ball_speed_x = 4
            self.ball_speed_y = 4
        elif DIFFICULTY_LEVEL == 2:
            self.ball_speed_x = 6
            self.ball_speed_y = 6
        elif DIFFICULTY_LEVEL == 3:
            self.ball_speed_x = 8
            self.ball_speed_y = 8
        elif DIFFICULTY_LEVEL == 4:
            self.ball_speed_x = 12
            self.ball_speed_y = 12
        self.direction_ball = random.randint(1, 2)
        self.ball = arcade.Sprite("pictures/tennball.png", scale=0.025)
        self.ball.center_x = SCREEN_WIDTH_GAME // 2
        self.ball.center_y = SCREEN_HEIGHT_GAME // 2
        self.all_sprites.append(self.ball)
        self.wall_player_list = arcade.SpriteList()
        self.wall_player_list.append(self.player_sprite_1)
        self.wall_player_list.append(self.player_sprite_2)

        self.leave_button_sprite = arcade.Sprite("pictures/botton.png", scale=0.5)
        self.leave_button_sprite.center_x = SCREEN_WIDTH_GAME // 2
        self.leave_button_sprite.center_y = 30
        self.all_sprites.append(self.leave_button_sprite)

    def on_show_view(self):
        self.window.set_size(SCREEN_WIDTH_GAME, SCREEN_HEIGHT_GAME)

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.leave_button_sprite.collides_with_point((x, y)):
            game_view = SecondView()
            self.window.show_view(game_view)

    def on_update(self, delta_time):
        dx1, dy1 = 0, 0
        dx2, dy2 = 0, 0
        moving1 = False
        moving2 = False

        # Определяем направление движения
        if arcade.key.W in self.keys_pressed:
            dy1 = self.player1_speed * delta_time
            moving1 = True
        if arcade.key.S in self.keys_pressed:
            dy1 = -self.player1_speed * delta_time
            moving1 = True
        if arcade.key.UP in self.keys_pressed:
            dy2 = self.player_speed * delta_time
            moving2 = True
        if arcade.key.DOWN in self.keys_pressed:
            dy2 = -self.player_speed * delta_time
            moving2 = True

        # Сохраняем старые позиции
        old_x1, old_y1 = self.hero_1_x, self.hero_1_y
        old_x2, old_y2 = self.hero_2_x, self.hero_2_y

        # Пробуем переместить игроков
        self.hero_1_y += dy1
        self.hero_2_y += dy2

        # Обновляем позиции спрайтов
        self.player_sprite_1.center_x = self.hero_1_x
        self.player_sprite_1.center_y = self.hero_1_y
        self.player_sprite_2.center_x = self.hero_2_x
        self.player_sprite_2.center_y = self.hero_2_y

        # Проверяем столкновения игрока 1 со стенами
        wall_collision_1 = False
        for wall in self.wall_list:
            if arcade.check_for_collision(self.player_sprite_1, wall):
                wall_collision_1 = True
                break

        # Проверяем столкновения игрока 2 со стенами
        wall_collision_2 = False
        for wall in self.wall_list:
            if arcade.check_for_collision(self.player_sprite_2, wall):
                wall_collision_2 = True
                break

        wall_collision_ball = False
        place_location = ""
        for wall in self.wall_player_list:
            if arcade.check_for_collision(self.ball, wall):
                wall_collision_ball = True
                place_location = "player"
                break
        for wall in self.wall_list:
            if arcade.check_for_collision(self.ball, wall):
                wall_collision_ball = True
                place_location = "wall"
                break

        # Если было столкновение, возвращаем игрока на старую позицию
        if wall_collision_1:
            self.hero_1_x, self.hero_1_y = old_x1, old_y1
            self.player_sprite_1.center_x = self.hero_1_x
            self.player_sprite_1.center_y = self.hero_1_y

        if wall_collision_2:
            self.hero_2_x, self.hero_2_y = old_x2, old_y2
            self.player_sprite_2.center_x = self.hero_2_x
            self.player_sprite_2.center_y = self.hero_2_y

        if wall_collision_ball:
            if place_location == "player":
                self.ball_speed_x *= -1
            elif place_location == "wall":
                self.ball_speed_y *= -1
            wall_collision_ball = False
            place_location = ""

        # Ограничение в пределах экрана по горизонтали
        if self.hero_1_x < 20:
            self.hero_1_x = 20
        if self.hero_1_x > SCREEN_WIDTH_GAME - 20:
            self.hero_1_x = SCREEN_WIDTH_GAME - 20
        if self.hero_2_x < 20:
            self.hero_2_x = 20
        if self.hero_2_x > SCREEN_WIDTH_GAME - 20:
            self.hero_2_x = SCREEN_WIDTH_GAME - 20

        # Ограничение в пределах экрана по вертикали (дополнительная защита)
        if self.hero_1_y < 100:  # Минимум 100 пикселей от нижнего края
            self.hero_1_y = 100
        if self.hero_1_y > SCREEN_HEIGHT_GAME - 100:  # Максимум 100 пикселей от верхнего края
            self.hero_1_y = SCREEN_HEIGHT_GAME - 100
        if self.hero_2_y < 100:
            self.hero_2_y = 100
        if self.hero_2_y > SCREEN_HEIGHT_GAME - 100:
            self.hero_2_y = SCREEN_HEIGHT_GAME - 100

        self.player_sprite_1.center_x = self.hero_1_x
        self.player_sprite_1.center_y = self.hero_1_y
        self.player_sprite_2.center_x = self.hero_2_x
        self.player_sprite_2.center_y = self.hero_2_y

        # Обновление анимации
        if moving1:
            self.time_since_last_frame_1 += delta_time
            if self.time_since_last_frame_1 >= self.frame_duration_1:
                self.time_since_last_frame_1 = 0
                self.current_texture_1 = (self.current_texture_1 + 1) % len(self.player_1_textures)
                self.player_sprite_1.texture = self.player_1_textures[self.current_texture_1]
        else:
            self.player_sprite_1.texture = self.player_1_textures[0]
            self.current_texture_1 = 0
            self.time_since_last_frame_1 = 0

        if moving2:
            self.time_since_last_frame_2 += delta_time
            if self.time_since_last_frame_2 >= self.frame_duration_2:
                self.time_since_last_frame_2 = 0
                self.current_texture_2 = (self.current_texture_2 + 1) % len(self.player_2_textures)
                self.player_sprite_2.texture = self.player_2_textures[self.current_texture_2]
        else:
            self.player_sprite_2.texture = self.player_2_textures[0]
            self.current_texture_2 = 0
            self.time_since_last_frame_2 = 0

        #мячик
        if self.direction_ball == 1:
            self.ball.center_x -= self.ball_speed_x
            self.ball.center_y -= self.ball_speed_y
        elif self.direction_ball == 2:
            self.ball.center_x += self.ball_speed_x
            self.ball.center_y += self.ball_speed_y



        global WINNER
        if self.ball.center_x < (-150):
            self.ball.center_x = SCREEN_WIDTH_GAME // 2
            self.ball.center_y = SCREEN_HEIGHT_GAME // 2
            self.count_2 += 1
        elif self.ball.center_x > (SCREEN_WIDTH_GAME + 150):
            self.ball.center_x = SCREEN_WIDTH_GAME // 2
            self.ball.center_y = SCREEN_HEIGHT_GAME // 2
            self.count_1 += 1
        if self.count_1 == 5:
            WINNER = "player 1"
            with open("score.txt", "w", encoding="utf-8-sig") as f:
                if DIFFICULTY_LEVEL == 1:
                    f.write(f"{SCORE[0] + 1}\n")
                    f.write(f"{SCORE[1]}")
                elif DIFFICULTY_LEVEL == 2:
                    f.write(f"{SCORE[0] + 3}\n")
                    f.write(f"{SCORE[1]}")
                elif DIFFICULTY_LEVEL == 3:
                    f.write(f"{SCORE[0] + 5}\n")
                    f.write(f"{SCORE[1]}")
                elif DIFFICULTY_LEVEL == 4:
                    f.write(f"{SCORE[0] + 7}\n")
                    f.write(f"{SCORE[1]}")
            game_view = EndView()
            self.window.show_view(game_view)
        elif self.count_2 == 5:
            WINNER = "player 2"
            with open("score.txt", "w", encoding="utf-8-sig") as f:
                if DIFFICULTY_LEVEL == 1:
                    f.write(f"{SCORE[0]}\n")
                    f.write(f"{SCORE[1] + 1}")
                elif DIFFICULTY_LEVEL == 2:
                    f.write(f"{SCORE[0]}\n")
                    f.write(f"{SCORE[1] + 3}")
                elif DIFFICULTY_LEVEL == 3:
                    f.write(f"{SCORE[0]}\n")
                    f.write(f"{SCORE[1] + 5}")
                elif DIFFICULTY_LEVEL == 4:
                    f.write(f"{SCORE[0]}\n")
                    f.write(f"{SCORE[1] + 7}")
            game_view = EndView()
            self.window.show_view(game_view)



    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(SCREEN_WIDTH_GAME // 2, SCREEN_HEIGHT_GAME // 2, SCREEN_WIDTH_GAME, SCREEN_HEIGHT_GAME))
        # Сначала стены
        self.wall_list.draw()
        self.all_sprites.draw()  # Потом игроки
        """self.ball.draw()"""
        score_text = arcade.Text(f"{self.count_1} : {self.count_2}", SCREEN_WIDTH_GAME // 2,
            SCREEN_HEIGHT_GAME - 60,
            arcade.color.YELLOW_ROSE,
            font_size=48,
            font_name="Impact",
            anchor_x="center",
            bold=False)
        score_text.draw()

        leave_text = arcade.Text("LEAVE",SCREEN_WIDTH_GAME // 2, 6,
            arcade.color.YELLOW_ROSE,
            font_size=48,
            font_name="Impact",
            anchor_x="center",
            bold=False)
        leave_text.draw()

        player_1_text = arcade.Text("player 1", 100,
                                 SCREEN_HEIGHT_GAME - 50,
                                 arcade.color.YELLOW_ROSE,
                                 font_size=40,
                                 font_name="Impact",
                                 anchor_x="center",
                                 bold=False)
        player_2_text = arcade.Text("player 2", SCREEN_WIDTH_GAME - 100,
                                    SCREEN_HEIGHT_GAME - 50,
                                    arcade.color.YELLOW_ROSE,
                                    font_size=40,
                                    font_name="Impact",
                                    anchor_x="center",
                                    bold=False)
        score_text.draw()
        player_1_text.draw()
        player_2_text.draw()


class EndView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.player = GameWindow.player
        # параметры пульсации текста
        self.time_elapsed = 0
        self.pulse_speed = 7
        self.pulse_min_scale = 0.9
        self.pulse_max_scale = 1.5
        # создание списка спрайтов
        self.all_sprites = arcade.SpriteList()
        # создание кнопок-спрайтов
        self.botton_sprite_1 = arcade.Sprite("pictures/rebot.png", scale=0.6)
        self.botton_sprite_1.center_x = SCREEN_WIDTH // 2 - 100
        self.botton_sprite_1.center_y = SCREEN_HEIGHT // 2 - 50
        self.all_sprites.append(self.botton_sprite_1)
        self.botton_sprite_2 = arcade.Sprite("pictures/menu.png", scale=0.6)
        self.botton_sprite_2.center_x = SCREEN_WIDTH // 2 + 100
        self.botton_sprite_2.center_y = SCREEN_HEIGHT // 2 - 50
        self.all_sprites.append(self.botton_sprite_2)

        with open("score.txt", "r", encoding="utf-8-sig") as f:
            k = f.readlines()
            SCORE.clear()
            for score in k:
                SCORE.append(int(score.rstrip()))

    def on_show_view(self):
        self.window.set_size(SCREEN_WIDTH, SCREEN_HEIGHT)

    def on_update(self, delta_time):
        # обновление времени
        self.time_elapsed += delta_time

    def on_draw(self):
        self.clear()
        # формула для пульсации текста
        pulse_factor = (math.sin(self.time_elapsed * self.pulse_speed) + 1) / 2  # от 0 до 1
        current_scale = self.pulse_min_scale + (self.pulse_max_scale - self.pulse_min_scale) * pulse_factor
        # значальный размер шрифта
        original_font_size = 50
        # обновление текста (для пульсации)
        pulsating_text = arcade.Text(
            f"{WINNER} WINS!",
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2 + 100,
            color=arcade.color.YELLOW_ROSE,
            font_size=int(original_font_size * current_scale),
            font_name="Impact",
            anchor_x="center",
            anchor_y="center",
            bold=False
        )
        # отрисовка пульсирующего текста
        pulsating_text.draw()
        self.all_sprites.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        # проверка нажатия на кнопку сложности
        if self.botton_sprite_1.collides_with_point((x, y)):
            game_view = GameWindow()
            self.window.show_view(game_view)
        elif self.botton_sprite_2.collides_with_point((x, y)):
            game_view = WelcomeView()
            self.window.show_view(game_view)


class SetupView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        # параметры пульсации текста
        self.time_elapsed = 0
        self.pulse_speed = 7
        self.pulse_min_scale = 0.9
        self.pulse_max_scale = 1.5
        # создание списка спрайтов
        self.all_sprites = arcade.SpriteList()
        # создание кнопок-спрайтов
        self.botton_sprite_1 = arcade.Sprite("pictures/botton.png", scale=0.8)
        self.botton_sprite_1.center_x = SCREEN_WIDTH // 2 - 130
        self.botton_sprite_1.center_y = SCREEN_HEIGHT // 2 - 50
        self.all_sprites.append(self.botton_sprite_1)
        self.botton_sprite_2 = arcade.Sprite("pictures/menu.png", scale=0.6)
        self.botton_sprite_2.center_x = SCREEN_WIDTH // 2 + 130
        self.botton_sprite_2.center_y = SCREEN_HEIGHT // 2 - 50
        self.all_sprites.append(self.botton_sprite_2)

        self.clear_text = arcade.Text(
            "Clear score",
            x=SCREEN_WIDTH // 2 - 130,
            y=SCREEN_HEIGHT // 2 - 50,
            color=arcade.color.YELLOW_ROSE,
            font_size=30,
            font_name="Impact",
            anchor_x="center",
            anchor_y="center",
            bold=False
        )

    def on_show_view(self):
        self.window.set_size(SCREEN_WIDTH, SCREEN_HEIGHT)

    def on_update(self, delta_time):
        # обновление времени
        self.time_elapsed += delta_time

    def on_draw(self):
        self.clear()
        # формула для пульсации текста
        pulse_factor = (math.sin(self.time_elapsed * self.pulse_speed) + 1) / 2  # от 0 до 1
        current_scale = self.pulse_min_scale + (self.pulse_max_scale - self.pulse_min_scale) * pulse_factor
        # значальный размер шрифта
        original_font_size = 50
        # обновление текста (для пульсации)
        pulsating_text = arcade.Text(
            f"SETUP",
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2 + 100,
            color=arcade.color.YELLOW_ROSE,
            font_size=int(original_font_size * current_scale),
            font_name="Impact",
            anchor_x="center",
            anchor_y="center",
            bold=False
        )
        # отрисовка пульсирующего текста
        pulsating_text.draw()
        self.all_sprites.draw()
        self.clear_text.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        # проверка нажатия на кнопку сложности
        if self.botton_sprite_1.collides_with_point((x, y)):
            with open("score.txt", "w", encoding="utf-8-sig") as f:
                f.write("0\n")
                f.write("0")
            with open("score.txt", "r", encoding="utf-8-sig") as f:
                k = f.readlines()
                SCORE.clear()
                for score in k:
                    SCORE.append(int(score.rstrip()))
        elif self.botton_sprite_2.collides_with_point((x, y)):
            game_view = WelcomeView()
            self.window.show_view(game_view)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    # Создаем и показываем первый View
    start_view = WelcomeView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()