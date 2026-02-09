import arcade
import arcade.gui
import math
import random
import os
import sqlite3

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
Round = 0
NAME_1 = ""
NAME_2 = ""


# ======= Класс для первого окна ======
class WelcomeView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        # текстовый обьект
        self.text_object = arcade.Text(
            "",
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2 + 155,
            color=arcade.color.YELLOW_ROSE,
            font_size=100,
            font_name="Impact",
            anchor_x="center",
            anchor_y="center",
            bold=False
        )

        self.text_score = arcade.Text(
            "Score",
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2,
            color=arcade.color.WHITE,
            font_size=50,
            font_name="Impact",
            anchor_x="center",
            anchor_y="center",
            bold=False
        )
        self.time_elapsed = 0

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

        self.tennball = arcade.Sprite("pictures/tennball.png", scale=0.15)
        self.tennball.center_x = SCREEN_WIDTH - 120
        self.tennball.center_y = SCREEN_HEIGHT - 120
        self.all_sprites.append(self.tennball)

        self.sprite_score = arcade.Sprite("pictures/botton.png", scale=0.8)
        self.sprite_score.center_x = SCREEN_WIDTH // 2
        self.sprite_score.center_y = SCREEN_HEIGHT // 2
        self.all_sprites.append(self.sprite_score)

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
        self.text_score.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        # проверка нажатия на стартовую кнопку
        if self.start_sprite.collides_with_point((x, y)):
            # открытие второго окна
            game_view = RoundView()
            self.window.show_view(game_view)
        elif self.sprite_score.collides_with_point((x, y)):
            game_view = ScoreView()
            self.window.show_view(game_view)


class ScoreView(arcade.View):
    def __init__(self):
        super().__init__()
        self.all_sprites = arcade.SpriteList()

        self.botton_sprite_menu = arcade.Sprite("pictures/menu.png", scale=0.5)
        self.botton_sprite_menu.center_x = SCREEN_WIDTH // 2
        self.botton_sprite_menu.center_y = SCREEN_HEIGHT // 2 - 240
        self.all_sprites.append(self.botton_sprite_menu)

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


# ====== Класс дл экрана выбора раундов =====
class RoundView(arcade.View):
    def __init__(self):
        super().__init__()
        self.all_sprites = arcade.SpriteList()
        # Создаем менеджер GUI
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Создаем поле ввода
        self.input_field = arcade.gui.UIInputText(
            x=SCREEN_WIDTH // 2 - 150, y=SCREEN_HEIGHT // 2 - 45, width=300, height=30, text=""
        )
        self.manager.add(self.input_field)

        self.botton_sprite = arcade.Sprite("pictures/botton.png", scale=0.5)
        self.botton_sprite.center_x = SCREEN_WIDTH // 2
        self.botton_sprite.center_y = SCREEN_HEIGHT // 2 - 190
        self.all_sprites.append(self.botton_sprite)

        self.round_text = arcade.Text(
            "Enter the number of rounds",
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2 + 90,
            color=arcade.color.YELLOW_ROSE,
            font_size=50,
            font_name="Impact",
            anchor_x="center",
            anchor_y="center",
            bold=False
        )

        self.Start_text = arcade.Text(
            "Start",
            x=SCREEN_WIDTH // 2,
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

    def on_mouse_press(self, x, y, button, modifiers):
        global Round
        # проверка нажатия на кнопку сложности
        if self.botton_sprite.collides_with_point((x, y)):
            Round = int(self.input_field.text)
            self.manager.disable()
            game_view = NameView()
            self.window.show_view(game_view)


class NameView(arcade.View):
    def __init__(self):
        super().__init__()
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
        self.botton_sprite.center_x = SCREEN_WIDTH // 2
        self.botton_sprite.center_y = SCREEN_HEIGHT // 2 - 190
        self.all_sprites.append(self.botton_sprite)

        self.round_text = arcade.Text(
            "ENTER PLAYER NAMES",
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2 + 90,
            color=arcade.color.YELLOW_ROSE,
            font_size=50,
            font_name="Impact",
            anchor_x="center",
            anchor_y="center",
            bold=False
        )

        self.Start_text = arcade.Text(
            "Start",
            x=SCREEN_WIDTH // 2,
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

    def on_mouse_press(self, x, y, button, modifiers):
        global Round
        global NAME_1
        global NAME_2
        # проверка нажатия на кнопку сложности
        if self.botton_sprite.collides_with_point((x, y)):
            NAME_1 = self.name_1_field.text
            NAME_2 = self.name_2_field.text
            self.manager.disable()
            game_view = SecondView()
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
        self.pulse_max_scale = 1.5

        # текстовые обьекты

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

        # создание списка спрайтов
        self.all_sprites = arcade.SpriteList()

        # создание кнопок-спрайтов

        self.botton_back = arcade.Sprite("pictures/botton.png", scale=0.5)
        self.botton_back.center_x = 100
        self.botton_back.center_y = SCREEN_HEIGHT // 2 - 202.5
        self.all_sprites.append(self.botton_back)

        self.botton_start = arcade.Sprite("pictures/startbutton.png", scale=0.25)
        self.botton_start.center_x = SCREEN_WIDTH // 2
        self.botton_start.center_y = SCREEN_HEIGHT // 2 - 202.5
        self.all_sprites.append(self.botton_start)

        self.setup_sprite = arcade.Sprite("pictures/setup.png", scale=0.10)
        self.setup_sprite.center_x = 40
        self.setup_sprite.center_y = SCREEN_HEIGHT - 40
        self.all_sprites.append(self.setup_sprite)

        self.instruction_button_sprite = arcade.Sprite("pictures/book.png", scale=0.3)
        self.instruction_button_sprite.center_x = SCREEN_WIDTH - 100
        self.instruction_button_sprite.center_y = SCREEN_HEIGHT - 80
        self.all_sprites.append(self.instruction_button_sprite)

        global SCORE
        global NAME_1
        global NAME_2
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

        self.score = arcade.Text(
            f"{NAME_1}-{SCORE[0]}  :  {SCORE[1]}-{NAME_2}",
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2,
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

    def on_draw(self):
        self.clear()

        # значения текстовых обьектов
        self.back_text.value = "BACK"

        # формула для пульсации текста
        pulse_factor = (math.sin(self.time_elapsed * self.pulse_speed) + 1) / 2  # от 0 до 1
        current_scale = self.pulse_min_scale + (self.pulse_max_scale - self.pulse_min_scale) * pulse_factor

        # значальный размер шрифта
        original_font_size = 100

        # обновление текста (для пульсации)
        pulsating_text = arcade.Text(
            "Score",
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2 + 175,
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
        self.back_text.draw()
        self.score.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        global DIFFICULTY_LEVEL
        global NAME_1
        global NAME_2
        global SCORE
        # проверка нажатия на кнопку сложности
        if self.botton_back.collides_with_point((x, y)):
            if SCORE != [0, 0] and SCORE != [] and SCORE != ['0', '0'] and len(SCORE) == 2:
                print(SCORE)
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
                print(SCORE)
            game_view = WelcomeView()
            self.window.show_view(game_view)
        elif self.botton_start.collides_with_point((x, y)):
            game_view = ThirdView()
            self.window.show_view(game_view)
        elif self.setup_sprite.collides_with_point((x, y)):
            game_view = SetupView_2()
            self.window.show_view(game_view)
        elif self.instruction_button_sprite.collides_with_point((x, y)):
            game_view = InstructionView()
            self.window.show_view(game_view)

    def on_show_view(self):
        self.window.set_size(SCREEN_WIDTH, SCREEN_HEIGHT)


class InstructionView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

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


class ThirdView(arcade.View):
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

        self.botton_sprite_5 = arcade.Sprite("pictures/botton.png", scale=0.5)
        self.botton_sprite_5.center_x = SCREEN_WIDTH // 2
        self.botton_sprite_5.center_y = SCREEN_HEIGHT // 2 - 202.5
        self.all_sprites.append(self.botton_sprite_5)

        self.setup_sprite = arcade.Sprite("pictures/setup.png", scale=0.10)
        self.setup_sprite.center_x = 40
        self.setup_sprite.center_y = SCREEN_HEIGHT - 40
        self.all_sprites.append(self.setup_sprite)

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
        elif self.botton_sprite_5.collides_with_point((x, y)):
            DIFFICULTY_LEVEL = 4
            game_view = GameWindow()
            self.window.show_view(game_view)
        elif self.setup_sprite.collides_with_point((x, y)):
            game_view = SetupView_3()
            self.window.show_view(game_view)

    def on_show_view(self):
        self.window.set_size(SCREEN_WIDTH, SCREEN_HEIGHT)


# ===== Класс для игры =======
class GameWindow(arcade.View):
    player = 1

    def __init__(self):
        super().__init__()
        self.count_1 = 0
        self.count_2 = 0
        arcade.set_background_color(arcade.color.BLACK)

        self.all_sprites = arcade.SpriteList()

        global DIFFICULTY_LEVEL
        global NAME_1
        global NAME_2

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

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.leave_button_sprite.collides_with_point((x, y)):
            game_view = ThirdView()
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
        if self.ball.center_x < (-150):
            self.ball.center_x = SCREEN_WIDTH_GAME // 2
            self.ball.center_y = SCREEN_HEIGHT_GAME // 2
            self.count_2 += 1
        elif self.ball.center_x > (SCREEN_WIDTH_GAME + 150):
            self.ball.center_x = SCREEN_WIDTH_GAME // 2
            self.ball.center_y = SCREEN_HEIGHT_GAME // 2
            self.count_1 += 1
        if self.count_1 == int(Round):
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
        elif self.count_2 == int(Round):
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

        score_text = arcade.Text(f"{self.count_1} : {self.count_2}", SCREEN_WIDTH_GAME // 2,
                                 SCREEN_HEIGHT_GAME - 60,
                                 arcade.color.YELLOW_ROSE,
                                 font_size=48,
                                 font_name="Impact",
                                 anchor_x="center",
                                 bold=False)
        score_text.draw()

        leave_text = arcade.Text("LEAVE", SCREEN_WIDTH_GAME // 2, 6,
                                 arcade.color.YELLOW_ROSE,
                                 font_size=48,
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

        self.win_sound = arcade.load_sound("pictures/soundofwictory.mp3")
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
        # конфети
        self.confetti_list = arcade.SpriteList()
        for _ in range(150):
            p = Confetti(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            self.confetti_list.append(p)

        self.sound_played = False

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
        self.confetti_list.update(delta_time)

    def on_draw(self):
        self.clear()
        # формула для пульсации текста
        pulse_factor = (math.sin(self.time_elapsed * self.pulse_speed) + 1) / 2  # от 0 до 1
        current_scale = self.pulse_min_scale + (self.pulse_max_scale - self.pulse_min_scale) * pulse_factor
        # значальный размер шрифта
        original_font_size = 50
        # обновление текста (для пульсации)
        if WINNER == "player 1":
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
                f"{NAME_2} WINS!",
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
        self.all_sprites.draw()
        # отрисовка конфети
        self.confetti_list.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        # проверка нажатия на кнопку сложности
        if self.botton_sprite_1.collides_with_point((x, y)):
            game_view = GameWindow()
            self.window.show_view(game_view)
        elif self.botton_sprite_2.collides_with_point((x, y)):
            game_view = SecondView()
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
            game_view = SecondView()
            self.window.show_view(game_view)


class SetupView_3(arcade.View):
    def __init__(self):
        super().__init__()
        self.all_sprites = arcade.SpriteList()
        # Создаем менеджер GUI
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Создаем поле ввода
        self.input_field = arcade.gui.UIInputText(
            x=SCREEN_WIDTH // 2 - 150, y=SCREEN_HEIGHT // 2 - 45, width=300, height=30, text=""
        )
        self.manager.add(self.input_field)

        self.botton_sprite = arcade.Sprite("pictures/botton.png", scale=0.5)
        self.botton_sprite.center_x = SCREEN_WIDTH // 2 - 100
        self.botton_sprite.center_y = SCREEN_HEIGHT // 2 - 190
        self.all_sprites.append(self.botton_sprite)

        self.botton_sprite_menu = arcade.Sprite("pictures/menu.png", scale=0.5)
        self.botton_sprite_menu.center_x = SCREEN_WIDTH // 2 + 100
        self.botton_sprite_menu.center_y = SCREEN_HEIGHT // 2 - 185
        self.all_sprites.append(self.botton_sprite_menu)

        self.round_text = arcade.Text(
            "Enter the number of rounds",
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2 + 90,
            color=arcade.color.YELLOW_ROSE,
            font_size=50,
            font_name="Impact",
            anchor_x="center",
            anchor_y="center",
            bold=False
        )

        self.Start_text = arcade.Text(
            "Change",
            x=SCREEN_WIDTH // 2 - 100,
            y=SCREEN_HEIGHT // 2 - 185,
            color=arcade.color.YELLOW_ROSE,
            font_size=20,
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

    def on_mouse_press(self, x, y, button, modifiers):
        global Round
        # проверка нажатия на кнопку сложности
        if self.botton_sprite.collides_with_point((x, y)):
            Round = int(self.input_field.text)
            self.manager.disable()
            game_view = ThirdView()
            self.window.show_view(game_view)
        elif self.botton_sprite_menu.collides_with_point((x, y)):
            game_view = SecondView()
            self.window.show_view(game_view)


class Confetti(arcade.Sprite):
    def __init__(self, x, y):
        # Создаем цветную текстуру
        color = random.choice([
            arcade.color.RED, arcade.color.GOLD, arcade.color.BLUE,
            arcade.color.GREEN, arcade.color.HOT_PINK, arcade.color.AZURE
        ])
        texture = arcade.make_soft_square_texture(10, color)
        super().__init__(texture)

        self.center_x = x
        self.center_y = y

        # Скорость и вращение
        self.change_x = random.uniform(-5, 5)
        self.change_y = random.uniform(2, 8)
        self.change_angle = random.uniform(-15, 15)

        # Таймер жизни
        self.lifetime = 5.0

    def update(self, delta_time: float = 1 / 60):
        # Движение
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Гравитация (пропорционально времени кадра)
        self.change_y -= 0.2
        self.angle += self.change_angle

        # Уменьшаем время жизни
        self.lifetime -= delta_time

        # Плавное исчезновение в последнюю секунду
        if self.lifetime <= 1.0:
            self.alpha = max(0, int(self.lifetime * 255))

        # Удаление
        if self.lifetime <= 0:
            self.remove_from_sprite_lists()


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    # Создаем и показываем первый View
    start_view = WelcomeView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
