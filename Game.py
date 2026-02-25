from arcade.particles import FadeParticle, Emitter, EmitInterval
import arcade.gui
import math
import random
import os
import sqlite3
import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_WIDTH_GAME = 1000
SCREEN_HEIGHT_GAME = 650
SCREEN_TITLE = "Pong"
SECOND_WINDOW_TITLE = "Game"
DIFFICULTY_LEVEL = 0
player = 0
WINNER = ""
SCORE = []
Round = 0
NAME_1 = ""
NAME_2 = ""
count_1 = None
count_2 = None
Plays = None
LANGUAGE = "ENG"

# ======= Класс для первого окна ======
class WelcomeView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        global LANGUAGE

        self.create_text_objects()

        self.time_elapsed = 0

        # параметры пульсации стартовой кнопки
        self.start_base_scale = 0.8
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
        self.tennisist_sprite_2.center_x = SCREEN_WIDTH - 130
        self.tennisist_sprite_2.center_y = 100
        self.all_sprites.append(self.tennisist_sprite_2)

        self.start_sprite = arcade.Sprite("pictures/botton.png", scale=0.8)
        self.start_sprite.center_x = SCREEN_WIDTH // 2
        self.start_sprite.center_y = SCREEN_HEIGHT - 200
        self.all_sprites.append(self.start_sprite)

        self.tennball = arcade.Sprite("pictures/tennball.png", scale=0.15)
        self.tennball.center_x = SCREEN_WIDTH - 120
        self.tennball.center_y = SCREEN_HEIGHT - 120
        self.all_sprites.append(self.tennball)

        self.sprite_score = arcade.Sprite("pictures/botton.png", scale=0.8)
        self.sprite_score.center_x = SCREEN_WIDTH // 2
        self.sprite_score.center_y = SCREEN_HEIGHT - 330
        self.all_sprites.append(self.sprite_score)

        self.eng_sprite = arcade.Sprite("pictures/botton.png", scale=0.5)
        self.eng_sprite.center_x = SCREEN_WIDTH // 2
        self.eng_sprite.center_y = 50
        self.all_sprites.append(self.eng_sprite)

        self.rus_sprite = arcade.Sprite("pictures/botton.png", scale=0.5)
        self.rus_sprite.center_x = SCREEN_WIDTH // 2
        self.rus_sprite.center_y = 120
        self.all_sprites.append(self.rus_sprite)

        self.eng_text = arcade.Text(
            "English",
            x=SCREEN_WIDTH // 2,
            y=50,
            color=arcade.color.YELLOW_ROSE,
            font_size=30,
            font_name="Impact",
            anchor_x="center",
            anchor_y="center",
            bold=False
        )

        self.rus_text = arcade.Text(
            "Русский",
            x=SCREEN_WIDTH // 2,
            y=120,
            color=arcade.color.YELLOW_ROSE,
            font_size=30,
            font_name="Impact",
            anchor_x="center",
            anchor_y="center",
            bold=False
        )

        self.choose_text = arcade.Text(
            "Choose language /  Выберите язык",
            x=SCREEN_WIDTH // 2,
            y=180,
            color=arcade.color.YELLOW_ROSE,
            font_size=18,
            font_name="Impact",
            anchor_x="center",
            anchor_y="center",
            bold=False
        )

    def create_text_objects(self):
        global LANGUAGE

        self.text_object = arcade.Text(
            "PONG",
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT - 70,
            color=arcade.color.YELLOW_ROSE,
            font_size=100,
            font_name="Impact",
            anchor_x="center",
            anchor_y="center",
            bold=False
        )

        if LANGUAGE == "ENG":
            self.text_score = arcade.Text(
                "Score",
                x=SCREEN_WIDTH // 2,
                y=SCREEN_HEIGHT - 330,
                color=arcade.color.WHITE,
                font_size=50,
                font_name="Impact",
                anchor_x="center",
                anchor_y="center",
                bold=False
            )

            self.text_start = arcade.Text(
                "START",
                x=SCREEN_WIDTH // 2,
                y=SCREEN_HEIGHT - 200,
                color=arcade.color.WHITE,
                font_size=50,
                font_name="Impact",
                anchor_x="center",
                anchor_y="center",
                bold=False
            )
        else:

            self.text_score = arcade.Text(
                "Счет",
                x=SCREEN_WIDTH // 2,
                y=SCREEN_HEIGHT - 330,
                color=arcade.color.WHITE,
                font_size=50,
                font_name="Impact",
                anchor_x="center",
                anchor_y="center",
                bold=False
            )

            self.text_start = arcade.Text(
                "СТАРТ",
                x=SCREEN_WIDTH // 2,
                y=SCREEN_HEIGHT - 200,
                color=arcade.color.WHITE,
                font_size=50,
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
        self.text_object.draw()
        self.text_score.draw()
        self.text_start.draw()
        self.eng_text.draw()
        self.rus_text.draw()
        self.choose_text.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        # проверка нажатия на стартовую кнопку
        if self.start_sprite.collides_with_point((x, y)):
            # открытие второго окна
            global Plays
            Plays = 1
            game_view = NameView()
            self.window.show_view(game_view)
        elif self.sprite_score.collides_with_point((x, y)):
            game_view = ScoreView()
            self.window.show_view(game_view)

        global LANGUAGE
        language_changed = False

        if self.eng_sprite.collides_with_point((x, y)):
            if LANGUAGE != "ENG":
                LANGUAGE = "ENG"
                language_changed = True
        elif self.rus_sprite.collides_with_point((x, y)):
            if LANGUAGE != "RUS":
                LANGUAGE = "RUS"
                language_changed = True

        if language_changed:
            self.create_text_objects()

class ScoreView(arcade.View):
    def __init__(self):
        super().__init__()
        self.all_sprites = arcade.SpriteList()
        global LANGUAGE

        self.botton_sprite_menu = arcade.Sprite("pictures/menu.png", scale=0.5)
        self.botton_sprite_menu.center_x = SCREEN_WIDTH // 2
        self.botton_sprite_menu.center_y = SCREEN_HEIGHT // 2 - 240
        self.all_sprites.append(self.botton_sprite_menu)

        if LANGUAGE == "ENG":
            self.round_text = arcade.Text(
                "Last 5 games",
                x=SCREEN_WIDTH // 2,
                y=SCREEN_HEIGHT // 2 + 240,
                color=arcade.color.YELLOW_ROSE,
                font_size=50,
                font_name="Impact",
                anchor_x="center",
                anchor_y="center",
                bold=False
            )
        else:
            self.round_text = arcade.Text(
                "Последние 5 игр",
                x=SCREEN_WIDTH // 2,
                y=SCREEN_HEIGHT // 2 + 240,
                color=arcade.color.YELLOW_ROSE,
                font_size=50,
                font_name="Impact",
                anchor_x="center",
                anchor_y="center",
                bold=False
            )

        con = sqlite3.connect("SCORE_end")
        cur = con.cursor()
        res = cur.execute("""
        SELECT ID FROM Score
        """).fetchall()
        numb = len(res)
        self.sprite_text = []
        y = [160, 80, 0, -80, -160]
        if len(res) >= 5:
            for k in range(0, 5):
                res = cur.execute(
                    f"""SELECT "1Player", "1Player_score", "2Player", "2Player_score" FROM Score WHERE ID = {numb - k}""").fetchone()
                round_text = arcade.Text(
                    f"{res[0]}    {res[1]} : {res[3]}    {res[2]}",
                    x=SCREEN_WIDTH // 2,
                    y=SCREEN_HEIGHT // 2 + y[k],
                    color=arcade.color.YELLOW_ROSE,
                    font_size=30,
                    font_name="Impact",
                    anchor_x="center",
                    anchor_y="center",
                    bold=False
                )
                self.sprite_text.append(round_text)
        else:
            for k in range(0, len(res)):
                res = cur.execute(
                    f"""SELECT "1Player", "1Player_score", "2Player", "2Player_score" FROM Score WHERE ID = {numb - k}""").fetchone()
                round_text = arcade.Text(
                    f"{res[0]}    {res[1]} : {res[3]}    {res[2]}",
                    x=SCREEN_WIDTH // 2,
                    y=SCREEN_HEIGHT // 2 + y[k],
                    color=arcade.color.YELLOW_ROSE,
                    font_size=30,
                    font_name="Impact",
                    anchor_x="center",
                    anchor_y="center",
                    bold=False
                )
                self.sprite_text.append(round_text)

    def on_draw(self):
        self.clear()
        self.all_sprites.draw()
        self.round_text.draw()
        for k in self.sprite_text:
            k.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.botton_sprite_menu.collides_with_point((x, y)):
            game_view = WelcomeView()
            self.window.show_view(game_view)


class NameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.flag = False
        global LANGUAGE

        self.all_sprites = arcade.SpriteList()
        # Создаем менеджер GUI
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Создаем поле ввода
        self.name_1_field = arcade.gui.UIInputText(
            x=80, y=SCREEN_HEIGHT // 2 - 45, width=300, height=30, text=""
        )
        self.manager.add(self.name_1_field)

        self.name_2_field = arcade.gui.UIInputText(
            x=SCREEN_WIDTH // 2 + 20, y=SCREEN_HEIGHT // 2 - 45, width=300, height=30, text=""
        )
        self.manager.add(self.name_2_field)

        self.botton_sprite = arcade.Sprite("pictures/botton.png", scale=0.5)
        self.botton_sprite.center_x = SCREEN_WIDTH // 2 + 80
        self.botton_sprite.center_y = SCREEN_HEIGHT // 2 - 190
        self.all_sprites.append(self.botton_sprite)
        self.botton_sprite_back = arcade.Sprite("pictures/botton.png", scale=0.5)
        self.botton_sprite_back.center_x = SCREEN_WIDTH // 2 - 80
        self.botton_sprite_back.center_y = SCREEN_HEIGHT // 2 - 190
        self.all_sprites.append(self.botton_sprite_back)

        if LANGUAGE == "ENG":
            self.round_text = arcade.Text(
                "New game\nEnter player names",
                x=SCREEN_WIDTH // 2,
                y=SCREEN_HEIGHT // 2 + 140,
                color=arcade.color.YELLOW_ROSE,
                font_size=50,
                font_name="Impact",
                anchor_x="center",
                anchor_y="center",
                bold=False,
                multiline=True,
                width=800,
                align="center",
            )

            self.Start_text = arcade.Text(
                "Start",
                x=SCREEN_WIDTH // 2 + 80,
                y=SCREEN_HEIGHT // 2 - 185,
                color=arcade.color.YELLOW_ROSE,
                font_size=40,
                font_name="Impact",
                anchor_x="center",
                anchor_y="center",
                bold=False
            )
            self.Back_text = arcade.Text(
                "Back",
                x=SCREEN_WIDTH // 2 - 80,
                y=SCREEN_HEIGHT // 2 - 185,
                color=arcade.color.YELLOW_ROSE,
                font_size=40,
                font_name="Impact",
                anchor_x="center",
                anchor_y="center",
                bold=False
            )
        else:
            self.round_text = arcade.Text(
                "Новая игра\nНазовите игроков",
                x=SCREEN_WIDTH // 2,
                y=SCREEN_HEIGHT // 2 + 140,
                color=arcade.color.YELLOW_ROSE,
                font_size=50,
                font_name="Impact",
                anchor_x="center",
                anchor_y="center",
                bold=False,
                multiline=True,
                width=800,
                align="center",
            )

            self.Start_text = arcade.Text(
                "Старт",
                x=SCREEN_WIDTH // 2 + 80,
                y=SCREEN_HEIGHT // 2 - 185,
                color=arcade.color.YELLOW_ROSE,
                font_size=40,
                font_name="Impact",
                anchor_x="center",
                anchor_y="center",
                bold=False
            )
            self.Back_text = arcade.Text(
                "Назад",
                x=SCREEN_WIDTH // 2 - 80,
                y=SCREEN_HEIGHT // 2 - 185,
                color=arcade.color.YELLOW_ROSE,
                font_size=40,
                font_name="Impact",
                anchor_x="center",
                anchor_y="center",
                bold=False
            )


    def on_draw(self):
        self.clear()
        self.manager.draw()
        self.all_sprites.draw()
        self.round_text.draw()
        self.Start_text.draw()
        self.Back_text.draw()
        if self.flag is True:
            self.error_text.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        global Round
        global NAME_1
        global NAME_2
        # проверка нажатия на кнопку сложности
        if self.botton_sprite.collides_with_point((x, y)):
            if len(self.name_1_field.text) + len(self.name_2_field.text) < 16:
                NAME_1 = self.name_1_field.text
                NAME_2 = self.name_2_field.text
                game_view = RoundView()
                self.window.show_view(game_view)
                self.manager.disable()
                self.flag = False
            else:
                if LANGUAGE == "ENG":
                    self.error_text = arcade.Text(
                        "Names are too big!",
                        x=SCREEN_WIDTH // 2,
                        y=SCREEN_HEIGHT // 2 - 85,
                        color=arcade.color.RED,
                        font_size=15,
                        font_name="Impact",
                        anchor_x="center",
                        anchor_y="center",
                        bold=False
                    )
                else:
                    self.error_text = arcade.Text(
                        "Имена слишком длинные!",
                        x=SCREEN_WIDTH // 2,
                        y=SCREEN_HEIGHT // 2 - 85,
                        color=arcade.color.RED,
                        font_size=15,
                        font_name="Impact",
                        anchor_x="center",
                        anchor_y="center",
                        bold=False
                    )
                self.flag = True
        elif self.botton_sprite_back.collides_with_point((x, y)):
            game_view = WelcomeView()
            self.window.show_view(game_view)
            self.manager.disable()


# ====== Класс дл экрана выбора раундов =====
class RoundView(arcade.View):
    def __init__(self):
        super().__init__()
        global Plays
        self.all_sprites = arcade.SpriteList()
        # Создаем менеджер GUI
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.exep = None

        # Создаем поле ввода
        self.input_field = arcade.gui.UIInputText(
            x=SCREEN_WIDTH // 2 - 150, y=SCREEN_HEIGHT // 2 - 45, width=300, height=30, text=""
        )
        self.manager.add(self.input_field)


        if Plays > 1:
            self.botton_sprite_back = arcade.Sprite("pictures/botton.png", scale=0.5)
            self.botton_sprite_back.center_x = SCREEN_WIDTH // 2 - 120
            self.botton_sprite_back.center_y = SCREEN_HEIGHT // 2 - 190
            self.botton_sprite_back.width = 350
            self.all_sprites.append(self.botton_sprite_back)

            self.botton_sprite = arcade.Sprite("pictures/botton.png", scale=0.5)
            self.botton_sprite.center_x = SCREEN_WIDTH // 2 + 160
            self.botton_sprite.center_y = SCREEN_HEIGHT // 2 - 190
            self.all_sprites.append(self.botton_sprite)
        else:
            self.botton_sprite_back = arcade.Sprite("pictures/botton.png", scale=0.5)
            self.botton_sprite_back.center_x = SCREEN_WIDTH // 2 - 80
            self.botton_sprite_back.center_y = SCREEN_HEIGHT // 2 - 190
            self.all_sprites.append(self.botton_sprite_back)

            self.botton_sprite = arcade.Sprite("pictures/botton.png", scale=0.5)
            self.botton_sprite.center_x = SCREEN_WIDTH // 2 + 80
            self.botton_sprite.center_y = SCREEN_HEIGHT // 2 - 190
            self.all_sprites.append(self.botton_sprite)

        if LANGUAGE == "ENG":
            self.round_text = arcade.Text(
                f"Round {Plays}\nWhat's the score until we play?",
                x=SCREEN_WIDTH // 2,
                y=SCREEN_HEIGHT // 2 + 100,
                color=arcade.color.YELLOW_ROSE,
                font_size=50,
                multiline=True,
                width=800,
                align="center",
                font_name="Impact",
                anchor_x="center",
                anchor_y="center",
                bold=False
            )

            if Plays > 1:
                self.Back_text = arcade.Text(
                    "Finish the game",
                    x=SCREEN_WIDTH // 2 - 120,
                    y=SCREEN_HEIGHT // 2 - 185,
                    color=arcade.color.YELLOW_ROSE,
                    font_size=30,
                    font_name="Impact",
                    anchor_x="center",
                    anchor_y="center",
                    bold=False
                )
                self.Start_text = arcade.Text(
                    "Next",
                    x=SCREEN_WIDTH // 2 + 160,
                    y=SCREEN_HEIGHT // 2 - 185,
                    color=arcade.color.YELLOW_ROSE,
                    font_size=40,
                    font_name="Impact",
                    anchor_x="center",
                    anchor_y="center",
                    bold=False
                )
            else:
                self.Back_text = arcade.Text(
                    "Back",
                    x=SCREEN_WIDTH // 2 - 80,
                    y=SCREEN_HEIGHT // 2 - 185,
                    color=arcade.color.YELLOW_ROSE,
                    font_size=40,
                    font_name="Impact",
                    anchor_x="center",
                    anchor_y="center",
                    bold=False
                )
                self.Start_text = arcade.Text(
                    "Next",
                    x=SCREEN_WIDTH // 2 + 80,
                    y=SCREEN_HEIGHT // 2 - 185,
                    color=arcade.color.YELLOW_ROSE,
                    font_size=40,
                    font_name="Impact",
                    anchor_x="center",
                    anchor_y="center",
                    bold=False
                )
        else:
            self.round_text = arcade.Text(
                f"Раунд {Plays}\nИграем до какого счета?",
                x=SCREEN_WIDTH // 2,
                y=SCREEN_HEIGHT // 2 + 100,
                color=arcade.color.YELLOW_ROSE,
                font_size=50,
                multiline=True,
                width=800,
                align="center",
                font_name="Impact",
                anchor_x="center",
                anchor_y="center",
                bold=False
            )

            if Plays > 1:
                self.Back_text = arcade.Text(
                    "Завершить игру",
                    x=SCREEN_WIDTH // 2 - 120,
                    y=SCREEN_HEIGHT // 2 - 185,
                    color=arcade.color.YELLOW_ROSE,
                    font_size=30,
                    font_name="Impact",
                    anchor_x="center",
                    anchor_y="center",
                    bold=False
                )
                self.Start_text = arcade.Text(
                    "Далее",
                    x=SCREEN_WIDTH // 2 + 160,
                    y=SCREEN_HEIGHT // 2 - 185,
                    color=arcade.color.YELLOW_ROSE,
                    font_size=40,
                    font_name="Impact",
                    anchor_x="center",
                    anchor_y="center",
                    bold=False
                )
            else:
                self.Back_text = arcade.Text(
                    "Назад",
                    x=SCREEN_WIDTH // 2 - 80,
                    y=SCREEN_HEIGHT // 2 - 185,
                    color=arcade.color.YELLOW_ROSE,
                    font_size=40,
                    font_name="Impact",
                    anchor_x="center",
                    anchor_y="center",
                    bold=False
                )
                self.Start_text = arcade.Text(
                    "Далее",
                    x=SCREEN_WIDTH // 2 + 80,
                    y=SCREEN_HEIGHT // 2 - 185,
                    color=arcade.color.YELLOW_ROSE,
                    font_size=40,
                    font_name="Impact",
                    anchor_x="center",
                    anchor_y="center",
                    bold=False
                )

    def on_mouse_press(self, x, y, button, modifiers):
        global Round
        global SCORE
        # проверка нажатия на кнопку сложности
        if self.botton_sprite.collides_with_point((x, y)):
            try:
                Round = int(self.input_field.text)
                self.manager.disable()
                game_view = SecondView()
                self.window.show_view(game_view)
                self.exep = False
            except ValueError:
                if LANGUAGE == "ENG":
                    self.error_text = arcade.Text(
                        "enter the number!",
                        x=SCREEN_WIDTH // 2,
                        y=SCREEN_HEIGHT // 2 - 85,
                        color=arcade.color.RED,
                        font_size=15,
                        font_name="Impact",
                        anchor_x="center",
                        anchor_y="center",
                        bold=False
                    )
                else:
                    self.error_text = arcade.Text(
                        "введите число!",
                        x=SCREEN_WIDTH // 2,
                        y=SCREEN_HEIGHT // 2 - 85,
                        color=arcade.color.RED,
                        font_size=15,
                        font_name="Impact",
                        anchor_x="center",
                        anchor_y="center",
                        bold=False
                    )
                self.exep = True
        elif self.botton_sprite_back.collides_with_point((x, y)):
            if Plays > 1:
                if SCORE != [0, 0] and SCORE != [] and SCORE != ['0', '0'] and len(SCORE) == 2:
                    con = sqlite3.connect("SCORE_end")
                    cur = con.cursor()
                    cur.execute(
                        'INSERT INTO Score ("1Player", "1Player_score", "2Player", "2Player_score") VALUES (?, ?, ?, ?)',
                        (NAME_1, SCORE[0], NAME_2, SCORE[1]))
                    con.commit()
                    with open("score.txt", "w", encoding="utf-8-sig") as f:
                        f.write("0\n")
                        f.write("0")
                    with open("score.txt", "r", encoding="utf-8-sig") as f:
                        k = f.readlines()
                        SCORE.clear()
                        for score in k:
                            SCORE.append(int(score.rstrip()))
                game_view = WinView()
                self.window.show_view(game_view)
            else:
                game_view = NameView()
                self.window.show_view(game_view)
            self.manager.disable()


    def on_draw(self):
        self.clear()
        self.manager.draw()
        self.all_sprites.draw()
        self.round_text.draw()
        self.Start_text.draw()
        self.Back_text.draw()
        if self.exep is True:
            self.error_text.draw()


class WinView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.player = GameWindow.player

        self.win_sound = arcade.load_sound("sounds/soundofwictory.mp3")
        # параметры пульсации текста
        self.time_elapsed = 0
        self.pulse_speed = 7
        self.pulse_min_scale = 0.9
        self.pulse_max_scale = 1.5

        self.confetti = Confetti(400, 300)

        self.sound_played = False

        # Планируем вызов функции через 5 секунд
        arcade.schedule_once(self.close_app, 3)

    def on_show_view(self):
        self.window.set_size(SCREEN_WIDTH, SCREEN_HEIGHT)
        if not self.sound_played:
            arcade.play_sound(self.win_sound)
            self.sound_played = True

    def on_hide_view(self):
        self.sound_played = False

    def on_update(self, delta_time):
        # обновление времени
        self.time_elapsed += delta_time
        # обновление конфети
        self.confetti.update(delta_time)

    def on_draw(self):
        self.clear()
        global SCORE
        # формула для пульсации текста
        pulse_factor = (math.sin(self.time_elapsed * self.pulse_speed) + 1) / 2  # от 0 до 1
        current_scale = self.pulse_min_scale + (self.pulse_max_scale - self.pulse_min_scale) * pulse_factor
        # значальный размер шрифта
        original_font_size = 50
        # обновление текста (для пульсации)
        if SCORE[0] > SCORE[1]:
            if LANGUAGE == "ENG":
                pulsating_text = arcade.Text(
                    f"{NAME_1} WINS!",
                    x=SCREEN_WIDTH // 2,
                    y=SCREEN_HEIGHT // 2 + 100,
                    color=arcade.color.YELLOW_ROSE,
                    font_size=int(original_font_size * current_scale),
                    font_name="Impact",
                    anchor_x="center",
                    anchor_y="center",
                    bold=False
                )
            else:
                pulsating_text = arcade.Text(
                    f"{NAME_1} ПОБЕЖДАЕТ!",
                    x=SCREEN_WIDTH // 2,
                    y=SCREEN_HEIGHT // 2 + 100,
                    color=arcade.color.YELLOW_ROSE,
                    font_size=int(original_font_size * current_scale),
                    font_name="Impact",
                    anchor_x="center",
                    anchor_y="center",
                    bold=False
                )
        else:
            if LANGUAGE == "ENG":
                pulsating_text = arcade.Text(
                    f"{NAME_2} WINS!",
                    x=SCREEN_WIDTH // 2,
                    y=SCREEN_HEIGHT // 2 + 100,
                    color=arcade.color.YELLOW_ROSE,
                    font_size=int(original_font_size * current_scale),
                    font_name="Impact",
                    anchor_x="center",
                    anchor_y="center",
                    bold=False)
            else:
                pulsating_text = arcade.Text(
                    f"{NAME_2} ПОБЕЖДАЕТ!",
                    x=SCREEN_WIDTH // 2,
                    y=SCREEN_HEIGHT // 2 + 100,
                    color=arcade.color.YELLOW_ROSE,
                    font_size=int(original_font_size * current_scale),
                    font_name="Impact",
                    anchor_x="center",
                    anchor_y="center",
                    bold=False)
        # отрисовка пульсирующего текста
        pulsating_text.draw()
        # отрисовка конфети
        self.confetti.draw()

    def close_app(self, delta_time):
        # Эта функция сработает через 5 секунд
        game_view = WelcomeView()
        self.window.show_view(game_view)




# ====== Класс для 2 окна =======
class SecondView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.music = arcade.load_sound("sounds/1min-2021-10-19_-_Funny_Bit_-_www.FesliyanStudios.com.mp3")
        self.sound_played = False
        self.s_player = None

        # создание списка спрайтов
        self.all_sprites = arcade.SpriteList()

        # создание кнопок-спрайтов

        self.botton_back = arcade.Sprite("pictures/botton.png", scale=0.5)
        self.botton_back.center_x = 100
        self.botton_back.center_y = SCREEN_HEIGHT // 2 - 202.5
        self.all_sprites.append(self.botton_back)

        self.instruction_button_sprite = arcade.Sprite("pictures/book.png", scale=0.15)
        self.instruction_button_sprite.center_x = SCREEN_WIDTH - 60
        self.instruction_button_sprite.center_y = SCREEN_HEIGHT - 55
        self.all_sprites.append(self.instruction_button_sprite)

        global SCORE
        if os.path.exists("score.txt"):
            with open("score.txt", "r", encoding="utf-8-sig") as f:
                k = f.readlines()
                SCORE.clear()
                for score in k:
                    SCORE.append(int(score.rstrip()))
        else:
            with open("score.txt", "w", encoding="utf-8-sig") as f:
                f.write("0\n")
                f.write("0")
            with open("score.txt", "r", encoding="utf-8-sig") as f:
                k = f.readlines()
                SCORE.clear()
                for score in k:
                    SCORE.append(int(score.rstrip()))


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
        if LANGUAGE == "ENG":
            self.back_text = arcade.Text(
                "Back",
                x=100,
                y=SCREEN_HEIGHT // 2 - 200,
                color=arcade.color.YELLOW_ROSE,
                font_size=30,
                font_name="Impact",
                anchor_x="center",
                anchor_y="center",
                bold=False
            )
        else:
            self.back_text = arcade.Text(
                "Назад",
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
        # создание кнопок-спрайтов
        self.botton_sprite_1 = arcade.Sprite("pictures/botton.png", scale=0.5)
        self.botton_sprite_1.center_x = SCREEN_WIDTH // 2
        self.botton_sprite_1.center_y = SCREEN_HEIGHT // 2 - 2.5 + 100
        self.botton_sprite_1.width = 220
        self.all_sprites.append(self.botton_sprite_1)
        self.botton_sprite_2 = arcade.Sprite("pictures/botton.png", scale=0.5)
        self.botton_sprite_2.center_x = SCREEN_WIDTH // 2
        self.botton_sprite_2.center_y = SCREEN_HEIGHT // 2 - 102.5 + 100
        self.botton_sprite_2.width = 220
        self.all_sprites.append(self.botton_sprite_2)
        self.botton_sprite_3 = arcade.Sprite("pictures/botton.png", scale=0.5)
        self.botton_sprite_3.center_x = SCREEN_WIDTH // 2
        self.botton_sprite_3.center_y = SCREEN_HEIGHT // 2 - 202.5 + 100
        self.botton_sprite_3.width = 220
        self.all_sprites.append(self.botton_sprite_3)
        self.botton_sprite_5 = arcade.Sprite("pictures/botton.png", scale=0.5)
        self.botton_sprite_5.center_x = SCREEN_WIDTH // 2
        self.botton_sprite_5.center_y = SCREEN_HEIGHT // 2 - 202.5
        self.botton_sprite_5.width = 220
        self.all_sprites.append(self.botton_sprite_5)

    def on_draw(self):
        self.clear()

        # значения текстовых обьектов

        # значения текстовых обьектов
        if LANGUAGE == "ENG":
            self.choose_text.value = "CHOOSE DIFFICULTY"
            self.easy_text.value = "EASY"
            self.medium_text.value = "MEDIUM"
            self.hard_text.value = "HARD"
            self.insane_text.value = "INSANE"
        else:
            self.choose_text.value = "ВЫБЕРИТЕ СЛОЖНОСТЬ"
            self.easy_text.value = "ЛЕГКИЙ"
            self.medium_text.value = "СРЕДНИЙ"
            self.hard_text.value = "СЛОЖНЫЙ"
            self.insane_text.value = "БЕЗУМНЫЙ"


        # значальный размер шрифта
        original_font_size = 35

        # обновление текста (для пульсации)
        if LANGUAGE == "ENG":
            pulsating_text = arcade.Text(
                "To start a round, select \ndifficulty level",
                x=SCREEN_WIDTH // 2,
                y=SCREEN_HEIGHT // 2 + 200,
                color=arcade.color.YELLOW_ROSE,
                font_size=int(original_font_size),
                font_name="Impact",
                anchor_x="center",
                anchor_y="center",
                bold=False,
                multiline = True,
                align="center",
                width=800
            )
        else:
            pulsating_text = arcade.Text(
                "Для начала раунда, выберите\nуровень сложности",
                x=SCREEN_WIDTH // 2,
                y=SCREEN_HEIGHT // 2 + 200,
                color=arcade.color.YELLOW_ROSE,
                font_size=int(original_font_size),
                font_name="Impact",
                anchor_x="center",
                anchor_y="center",
                bold=False,
                multiline=True,
                align="center",
                width=800
            )

        self.all_sprites.draw()

        # отрисовка текста кнопок
        self.easy_text.draw()
        self.medium_text.draw()
        self.hard_text.draw()
        self.back_text.draw()
        self.insane_text.draw()
        pulsating_text.draw()



    def on_mouse_press(self, x, y, button, modifiers):
        global DIFFICULTY_LEVEL
        global NAME_1
        global NAME_2
        global SCORE
        if self.botton_back.collides_with_point((x, y)):
            game_view = RoundView()
            self.window.show_view(game_view)
            if self.s_player:
                arcade.stop_sound(self.s_player)
        elif self.instruction_button_sprite.collides_with_point((x, y)):
            game_view = InstructionView()
            self.window.show_view(game_view)
            if self.s_player:
                arcade.stop_sound(self.s_player)
        elif self.botton_sprite_1.collides_with_point((x, y)):
            DIFFICULTY_LEVEL = 1
            game_view = GameWindow()
            self.window.show_view(game_view)
            if self.s_player:
                arcade.stop_sound(self.s_player)
        elif self.botton_sprite_2.collides_with_point((x, y)):
            DIFFICULTY_LEVEL = 2
            game_view = GameWindow()
            self.window.show_view(game_view)
            if self.s_player:
                arcade.stop_sound(self.s_player)
        elif self.botton_sprite_3.collides_with_point((x, y)):
            DIFFICULTY_LEVEL = 3
            game_view = GameWindow()
            self.window.show_view(game_view)
            if self.s_player:
                arcade.stop_sound(self.s_player)
        elif self.botton_sprite_5.collides_with_point((x, y)):
            DIFFICULTY_LEVEL = 4
            game_view = GameWindow()
            self.window.show_view(game_view)
            if self.s_player:
                arcade.stop_sound(self.s_player)

    def on_show_view(self):
        self.window.set_size(SCREEN_WIDTH, SCREEN_HEIGHT)
        if not self.sound_played:
            self.s_player = arcade.play_sound(self.music, loop=True)
            self.sound_played = True

    def on_hide_view(self):
            self.sound_played = False


class InstructionView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        if LANGUAGE == "ENG":
            instruction_lines = [
                "GAME INSTRUCTIONS",
                "",
                "WELCOME TO PONG!",
                "",
                "CONTROL:",
                "• Player on the left: W (up) and S (down) keys",
                "• Player on the right: arrows ↑ (up) and ↓ (down)",
                "",
                "RULES OF THE GAME:",
                "• Start the game by pressing START",
                "• The score is displayed at the top of the screen",
                "• Exit the game: LEAVE button",
                "",
                "DIFFICULTY LEVELS:",
                "• Light: Ball speed = 4",
                "• Medium: ball speed = 6",
                "• Hard: ball speed = 8",
                "• Insane: Ball speed = 12",
                "",
                "SCORING SYSTEM:",
                "• Easy: 1 point for a win",
                "• Medium: 3 points for a win",
                "• Hard: 5 points for a win",
                "• Insane: 7 points for a win",
                "",
                "The score is saved after each game.",
                "We wish you a good game!"
            ]
        else:
            instruction_lines = [
                "ИНСТРУКЦИЯ К ИГРЕ",
                "",
                "ДОБРО ПОЖАЛОВАТЬ В ПОНГ!",
                "",
                "УПРАВЛЕНИЕ:",
                "• Игрок слева: клавиши W (вверх) и S (вниз).",
                "• Игрок справа: стрелки ↑ (вверх) и ↓ (вниз)",
                "",
                "ПРАВИЛА ИГРЫ:",
                "• Начните игру, нажав кнопку START",
                "• Результат отображается в верхней части экрана",
                "• Выход из игры: кнопка ВЫЙТИ",
                "",
                "УРОВНИ СЛОЖНОСТИ:",
                "• Легкий: Скорость мяча = 4",
                "• Средний: скорость мяча = 6",
                "• Сложный: скорость мяча = 8",
                "• Безумный: скорость мяча = 8",
                "",
                "СИСТЕМА ОЧКОВ",
                "• Легкий: 1 очко за победу",
                "• Средний: 3 очка за победу",
                "• Сложный: 5 очков за победу",
                "• Безумный: 7 очков за победу",
                "",
                "Результат сохраняется после каждой игры",
                "Желаем вам удачной игры!"
            ]

        self.text_lines = list()
        start_y = SCREEN_HEIGHT - 50
        line_height = 17

        for i, line in enumerate(instruction_lines):
            font_size = 30 if i == 0 else (20 if i == 2 else 15)
            color = arcade.color.YELLOW_ROSE if i in [0, 2, 4, 8, 12, 16] else arcade.color.WHITE

            text = arcade.Text(
                line,
                x=SCREEN_WIDTH // 2,
                y=start_y - i * line_height,
                color=color,
                font_size=font_size,
                font_name="Arial" if i > 0 else "Impact",
                anchor_x="center",
                anchor_y="center",
                bold=(i in [0, 2, 4, 8, 12, 16])
            )
            self.text_lines.append(text)

        self.all_sprites = arcade.SpriteList()
        self.back_button = arcade.Sprite("pictures/botton.png", scale=0.5)
        self.back_button.center_x = SCREEN_WIDTH // 2
        self.back_button.center_y = 60
        self.all_sprites.append(self.back_button)

        if LANGUAGE == "ENG":
            self.back_text = arcade.Text(
                "BACK",
                x=SCREEN_WIDTH // 2,
                y=60,
                color=arcade.color.YELLOW_ROSE,
                font_size=25,
                font_name="Impact",
                anchor_x="center",
                anchor_y="center",
                bold=True
            )
        else:
            self.back_text = arcade.Text(
                "НАЗАД",
                x=SCREEN_WIDTH // 2,
                y=60,
                color=arcade.color.YELLOW_ROSE,
                font_size=25,
                font_name="Impact",
                anchor_x="center",
                anchor_y="center",
                bold=True
            )

    def on_draw(self):
        self.clear()

        for text in self.text_lines:
            text.draw()

        self.all_sprites.draw()
        self.back_text.draw()

    def on_show_view(self):
        self.window.set_size(SCREEN_WIDTH, SCREEN_HEIGHT)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.back_button.collides_with_point((x, y)):
            game_view = SecondView()
            self.window.show_view(game_view)


# ===== Класс для игры =======
class GameWindow(arcade.View):
    player = 1

    def __init__(self):
        super().__init__()
        global count_1
        global count_2
        count_1 = 0
        count_2 = 0
        arcade.set_background_color(arcade.color.BLACK)

        self.all_sprites = arcade.SpriteList()

        global DIFFICULTY_LEVEL
        global NAME_1
        global NAME_2

        self.music_player = None

        if DIFFICULTY_LEVEL == 1:
            self.texture = arcade.load_texture("pictures/cort.jfif")
            self.music = arcade.load_sound("sounds/easysound.mp3")
        if DIFFICULTY_LEVEL == 2:
            self.texture = arcade.load_texture("pictures/city.jpg")
            self.music = arcade.load_sound("sounds/mediumsound.mp3")
        if DIFFICULTY_LEVEL == 3:
            self.texture = arcade.load_texture("pictures/apocal.jpg")
            self.music = arcade.load_sound("sounds/hardsound.mp3")
        if DIFFICULTY_LEVEL == 4:
            self.texture = arcade.load_texture("pictures/newspace.png")
            self.music = arcade.load_sound("sounds/insanesound.mp3")

        self.player1_speed = 450
        self.player_speed = 450

        self.hero_1_x = SCREEN_WIDTH_GAME - 960
        self.hero_1_y = SCREEN_HEIGHT_GAME // 2

        self.hero_2_x = SCREEN_WIDTH_GAME - 40
        self.hero_2_y = SCREEN_HEIGHT_GAME // 2

        self.stick_width = 0.001
        self.stick_height = 100

        self.stick_1_x = self.hero_1_x + 10
        self.stick_1_y = self.hero_1_y
        self.stick_2_x = self.hero_2_x - 10
        self.stick_2_y = self.hero_2_y

        self.stick_1_sprite = arcade.SpriteSolidColor(self.stick_width, self.stick_height, arcade.color.WHITE)
        self.stick_1_sprite.center_x = self.stick_1_x
        self.stick_1_sprite.center_y = self.stick_1_y

        self.stick_2_sprite = arcade.SpriteSolidColor(self.stick_width, self.stick_height, arcade.color.WHITE)
        self.stick_2_sprite.center_x = self.stick_2_x
        self.stick_2_sprite.center_y = self.stick_2_y

        self.all_sprites.append(self.stick_1_sprite)
        self.all_sprites.append(self.stick_2_sprite)

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

        # мячик
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
        self.wall_player_list.append(self.stick_1_sprite)
        self.wall_player_list.append(self.stick_2_sprite)

        self.leave_button_sprite = arcade.Sprite("pictures/botton.png", scale=0.5)
        self.leave_button_sprite.center_x = SCREEN_WIDTH_GAME // 2
        self.leave_button_sprite.center_y = 30
        self.all_sprites.append(self.leave_button_sprite)

    def on_show_view(self):
        self.window.set_size(SCREEN_WIDTH_GAME, SCREEN_HEIGHT_GAME)
        self.music_player = arcade.play_sound(self.music, loop=True)

    def on_hide_view(self):
        if self.music_player:
            arcade.stop_sound(self.music_player)

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
        global count_1, count_2

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
        old_stick_x1 = self.stick_1_sprite.center_x
        old_stick_y1 = self.stick_1_sprite.center_y
        old_stick_x2 = self.stick_2_sprite.center_x
        old_stick_y2 = self.stick_2_sprite.center_y

        # Пробуем переместить игроков
        self.hero_1_y += dy1
        self.hero_2_y += dy2

        self.stick_1_sprite.center_y += dy1
        self.stick_2_sprite.center_y += dy2

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
        wall_stick_collision_1 = False
        for wall in self.wall_list:
            if arcade.check_for_collision(self.stick_1_sprite, wall):
                wall_stick_collision_1 = True
                break

        # Проверяем столкновения игрока 2 со стенами
        wall_collision_2 = False
        for wall in self.wall_list:
            if arcade.check_for_collision(self.player_sprite_2, wall):
                wall_collision_2 = True
                break
        wall_stick_collision_2 = False
        for wall in self.wall_list:
            if arcade.check_for_collision(self.stick_2_sprite, wall):
                wall_stick_collision_2 = True
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

        if wall_stick_collision_1:
            self.stick_1_sprite.center_y, self.stick_1_sprite.center_x = old_stick_y1, old_stick_x1

        if wall_collision_2:
            self.hero_2_x, self.hero_2_y = old_x2, old_y2
            self.player_sprite_2.center_x = self.hero_2_x
            self.player_sprite_2.center_y = self.hero_2_y

        if wall_stick_collision_2:
            self.stick_2_sprite.center_y, self.stick_2_sprite.center_x = old_stick_y2, old_stick_x2

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

        # мячик
        if self.direction_ball == 1:
            self.ball.center_x -= self.ball_speed_x
            self.ball.center_y -= self.ball_speed_y
        elif self.direction_ball == 2:
            self.ball.center_x += self.ball_speed_x
            self.ball.center_y += self.ball_speed_y

        global WINNER
        global Round
        global count_2
        global count_1

        if self.ball.center_x < (-150):
            self.ball.center_x = SCREEN_WIDTH_GAME // 2
            self.ball.center_y = SCREEN_HEIGHT_GAME // 2
            count_2 += 1
        elif self.ball.center_x > (SCREEN_WIDTH_GAME + 150):
            self.ball.center_x = SCREEN_WIDTH_GAME // 2
            self.ball.center_y = SCREEN_HEIGHT_GAME // 2
            count_1 += 1

        if count_1 == int(Round):
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
        elif count_2 == int(Round):
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
        arcade.draw_texture_rect(self.texture,
                                 arcade.rect.XYWH(SCREEN_WIDTH_GAME // 2, SCREEN_HEIGHT_GAME // 2, SCREEN_WIDTH_GAME,
                                                  SCREEN_HEIGHT_GAME))
        # Сначала стены
        self.wall_list.draw()
        self.all_sprites.draw()  # Потом игроки

        score_text = arcade.Text(f"{count_1} : {count_2}", SCREEN_WIDTH_GAME // 2,
                                 SCREEN_HEIGHT_GAME - 60,
                                 arcade.color.YELLOW_ROSE,
                                 font_size=48,
                                 font_name="Impact",
                                 anchor_x="center",
                                 bold=False)
        score_text.draw()

        if LANGUAGE == "ENG":
            leave_text = arcade.Text("LEAVE", SCREEN_WIDTH_GAME // 2, 8,
                                     arcade.color.YELLOW_ROSE,
                                     font_size=30,
                                     font_name="Impact",
                                     anchor_x="center",
                                     bold=False)
        else:
            leave_text = arcade.Text("ВЫЙТИ", SCREEN_WIDTH_GAME // 2, 8,
                                     arcade.color.YELLOW_ROSE,
                                     font_size=30,
                                     font_name="Impact",
                                     anchor_x="center",
                                     bold=False)
        leave_text.draw()

        player_1_text = arcade.Text(f"{NAME_1}", 100,
                                    SCREEN_HEIGHT_GAME - 50,
                                    arcade.color.YELLOW_ROSE,
                                    font_size=40,
                                    font_name="Impact",
                                    anchor_x="center",
                                    bold=False)
        player_2_text = arcade.Text(f"{NAME_2}", SCREEN_WIDTH_GAME - 100,
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
        self.botton_sprite_1 = arcade.Sprite("pictures/botton.png", scale=0.7)
        self.botton_sprite_1.center_x = SCREEN_WIDTH // 2 - 200
        self.botton_sprite_1.center_y = SCREEN_HEIGHT // 2 - 200
        self.botton_sprite_1.width = 350
        self.all_sprites.append(self.botton_sprite_1)
        self.botton_sprite_2 = arcade.Sprite("pictures/botton.png", scale=0.7)
        self.botton_sprite_2.center_x = SCREEN_WIDTH // 2 + 200
        self.botton_sprite_2.center_y = SCREEN_HEIGHT // 2 - 200
        self.botton_sprite_2.width = 350
        self.all_sprites.append(self.botton_sprite_2)

        self.setup_sprite = arcade.Sprite("pictures/setup.png", scale=0.10)
        self.setup_sprite.center_x = 40
        self.setup_sprite.center_y = SCREEN_HEIGHT - 40
        self.all_sprites.append(self.setup_sprite)

        if LANGUAGE == "RUS":
            self.text_1 = arcade.Text(
                f"Еще один раунд",
                x=SCREEN_WIDTH // 2 - 200,
                y=SCREEN_HEIGHT // 2 - 200,
                color=arcade.color.YELLOW_ROSE,
                font_size=30,
                font_name="Impact",
                anchor_x="center",
                anchor_y="center",
                bold=False
            )
            self.text_2 = arcade.Text(
                f"Завершить игру",
                x=SCREEN_WIDTH // 2 + 200,
                y=SCREEN_HEIGHT // 2 - 200,
                color=arcade.color.YELLOW_ROSE,
                font_size=30,
                font_name="Impact",
                anchor_x="center",
                anchor_y="center",
                bold=False
            )
        else:
            self.text_1 = arcade.Text(
                f"One more round",
                x=SCREEN_WIDTH // 2 - 200,
                y=SCREEN_HEIGHT // 2 - 200,
                color=arcade.color.YELLOW_ROSE,
                font_size=30,
                font_name="Impact",
                anchor_x="center",
                anchor_y="center",
                bold=False
            )
            self.text_2 = arcade.Text(
                f"Finish the game",
                x=SCREEN_WIDTH // 2 + 200,
                y=SCREEN_HEIGHT // 2 - 200,
                color=arcade.color.YELLOW_ROSE,
                font_size=30,
                font_name="Impact",
                anchor_x="center",
                anchor_y="center",
                bold=False
            )


        global NAME_1
        global NAME_2
        global SCORE
        global Plays

        with open("score.txt", "r", encoding="utf-8-sig") as f:
            k = f.readlines()
            SCORE.clear()
            for score in k:
                SCORE.append(int(score.rstrip()))

        if LANGUAGE == "RUS":
            self.score_gl = arcade.Text(
                f"Общий счет за {Plays} раундов\n{NAME_1}-{SCORE[0]}  :  {SCORE[1]}-{NAME_2}",
                x=SCREEN_WIDTH // 2,
                y=SCREEN_HEIGHT // 2 - 25,
                color=arcade.color.YELLOW_ROSE,
                font_size=40,
                font_name="Impact",
                anchor_x="center",
                anchor_y="center",
                bold=False,
                align="center",
                multiline=True,
                width=800
            )

            global count_1
            global count_2
            self.score_end = arcade.Text(
                f"Раунд завершен со счетом\n{NAME_1}-{count_1}  :  {count_2}-{NAME_2}",
                x=SCREEN_WIDTH // 2,
                y=SCREEN_HEIGHT // 2 + 150,
                color=arcade.color.YELLOW_ROSE,
                font_size=40,
                font_name="Impact",
                anchor_x="center",
                anchor_y="center",
                bold=False,
                align="center",
                multiline=True,
                width=800
            )
        else:
            self.score_gl = arcade.Text(
                f"Total score for {Plays} rounds\n{NAME_1}-{SCORE[0]}  :  {SCORE[1]}-{NAME_2}",
                x=SCREEN_WIDTH // 2,
                y=SCREEN_HEIGHT // 2 - 25,
                color=arcade.color.YELLOW_ROSE,
                font_size=40,
                font_name="Impact",
                anchor_x="center",
                anchor_y="center",
                bold=False,
                align="center",
                multiline=True,
                width=800
            )

            self.score_end = arcade.Text(
                f"The round ended with a score of\n{NAME_1}-{count_1}  :  {count_2}-{NAME_2}",
                x=SCREEN_WIDTH // 2,
                y=SCREEN_HEIGHT // 2 + 150,
                color=arcade.color.YELLOW_ROSE,
                font_size=40,
                font_name="Impact",
                anchor_x="center",
                anchor_y="center",
                bold=False,
                align="center",
                multiline=True,
                width=800
            )

    def on_show_view(self):
        self.window.set_size(SCREEN_WIDTH, SCREEN_HEIGHT)


    def on_update(self, delta_time):
        # обновление времени
        self.time_elapsed += delta_time

    def on_draw(self):
        self.clear()
        self.all_sprites.draw()
        self.score_gl.draw()
        self.score_end.draw()
        # отрисовка конфети
        self.text_1.draw()
        self.text_2.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        # проверка нажатия на кнопку сложности
        if self.botton_sprite_1.collides_with_point((x, y)):
            global Plays
            Plays += 1
            game_view = RoundView()
            self.window.show_view(game_view)
        elif self.botton_sprite_2.collides_with_point((x, y)):
            global DIFFICULTY_LEVEL
            global NAME_1
            global NAME_2
            global SCORE
            if SCORE != [0, 0] and SCORE != [] and SCORE != ['0', '0'] and len(SCORE) == 2:
                con = sqlite3.connect("SCORE_end")
                cur = con.cursor()
                cur.execute(
                    'INSERT INTO Score ("1Player", "1Player_score", "2Player", "2Player_score") VALUES (?, ?, ?, ?)',
                    (NAME_1, SCORE[0], NAME_2, SCORE[1]))
                con.commit()
                with open("score.txt", "w", encoding="utf-8-sig") as f:
                    f.write("0\n")
                    f.write("0")
                with open("score.txt", "r", encoding="utf-8-sig") as f:
                    k = f.readlines()
                    SCORE.clear()
                    for score in k:
                        SCORE.append(int(score.rstrip()))
            Plays = None
            game_view = WinView()
            self.window.show_view(game_view)
        elif self.setup_sprite.collides_with_point((x, y)):
            game_view = SetupView_2()
            self.window.show_view(game_view)


class SetupView_2(arcade.View):
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

        if LANGUAGE == "ENG":
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
        else:
            self.clear_text = arcade.Text(
                "Обнулить счет",
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
        if LANGUAGE == "ENG":
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
        else:
            pulsating_text = arcade.Text(
                f"НАСТРОЙКИ",
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
            game_view = EndView()
            self.window.show_view(game_view)


class Confetti(Emitter):
    def __init__(self, x, y):
        # Набор цветов
        colors = [
            arcade.color.RED, arcade.color.GOLD, arcade.color.BLUE,
            arcade.color.GREEN, arcade.color.HOT_PINK, arcade.color.AZURE
        ]

        # Настраиваем эмиттер через super()
        super().__init__(
            center_xy=(x, y),
            emit_controller=EmitInterval(0.02),
            particle_factory=lambda e: FadeParticle(
                scale=2.0,
                filename_or_texture=arcade.make_soft_square_texture(10, random.choice(colors)),
                change_xy=(random.uniform(-5, 5), random.uniform(2, 8)),
                lifetime=random.uniform(3.0, 5.0),
                mutation_callback=self.confetti_physics  # Наша гравитация и вращение
            )
        )

    def confetti_physics(self, p):
        # Гравитация (change_y -= 0.2)
        p.change_y -= 0.2



def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    # Создаем и показываем первый View
    start_view = WelcomeView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()