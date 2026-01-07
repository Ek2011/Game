import arcade
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Cross"
SECOND_WINDOW_TITLE = "Second Window"


class SecondWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.GRAY)

        self.time_elapsed = 0
        self.pulse_speed = 7
        self.pulse_min_scale = 0.9
        self.pulse_max_scale = 1.1

        self.choose_text = arcade.Text(
            "",
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2 + 100,
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
            y=SCREEN_HEIGHT // 2,
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
            y=SCREEN_HEIGHT // 2 - 100,
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
            y=SCREEN_HEIGHT // 2 - 200,
            color=arcade.color.YELLOW_ROSE,
            font_size=30,
            font_name="Impact",
            anchor_x="center",
            anchor_y="center",
            bold=False
        )

    def on_update(self, delta_time):
        self.time_elapsed += delta_time

    def on_draw(self):
        self.clear()

        arcade.draw_lbwh_rectangle_filled(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 - 35, 150, 70,
                                          arcade.color.TANGERINE)
        arcade.draw_lbwh_rectangle_filled(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 - 135, 150, 70,
                                          arcade.color.TANGERINE)
        arcade.draw_lbwh_rectangle_filled(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 - 235, 150, 70,
                                          arcade.color.TANGERINE)

        self.choose_text.value = "CHOOSE DIFFICULTY"
        self.easy_text.value = "EASY"
        self.medium_text.value = "MEDIUM"
        self.hard_text.value = "HARD"

        pulse_factor = (math.sin(self.time_elapsed * self.pulse_speed) + 1) / 2  # от 0 до 1
        current_scale = self.pulse_min_scale + (self.pulse_max_scale - self.pulse_min_scale) * pulse_factor

        original_font_size = 50

        pulsating_text = arcade.Text(
            "CHOOSE DIFFICULTY",
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2 + 100,
            color=arcade.color.YELLOW_ROSE,
            font_size=int(original_font_size * current_scale),
            font_name="Impact",
            anchor_x="center",
            anchor_y="center",
            bold=False
        )

        pulsating_text.draw()

        self.easy_text.draw()
        self.medium_text.draw()
        self.hard_text.draw()



class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.GRAY)

        self.text_object = arcade.Text(
            "",
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2 + 100,
            color=arcade.color.YELLOW_ROSE,
            font_size=100,
            font_name="Impact",
            anchor_x="center",
            anchor_y="center",
            bold=False
        )
        self.time_elapsed = 0

        self.start_base_scale = 0.3
        self.pulse_amplitude = 0.02
        self.pulse_speed = 8

        self.all_sprites = arcade.SpriteList()

        self.tennisist_sprite_1 = arcade.Sprite("tennisist.png", scale=0.35)
        self.tennisist_sprite_1.center_x = SCREEN_WIDTH // 3
        self.tennisist_sprite_1.center_y = 300
        self.all_sprites.append(self.tennisist_sprite_1)

        self.tennisist_sprite_2 = arcade.Sprite("tenn3.png", scale=0.2)
        self.tennisist_sprite_2.center_x = SCREEN_WIDTH - 150
        self.tennisist_sprite_2.center_y = 100
        self.all_sprites.append(self.tennisist_sprite_2)

        self.start_sprite = arcade.Sprite("startbutton.png", scale=0.3)
        self.start_sprite.center_x = SCREEN_WIDTH // 2
        self.start_sprite.center_y = SCREEN_HEIGHT // 2 - 50
        self.all_sprites.append(self.start_sprite)

    def on_update(self, delta_time):
        self.time_elapsed += delta_time

        pulse_scale = self.start_base_scale + self.pulse_amplitude * math.sin(self.pulse_speed * self.time_elapsed)
        self.start_sprite.scale = pulse_scale

    def on_draw(self):
        self.clear()
        self.all_sprites.draw()

        self.text_object.value = "PONG"
        self.text_object.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if (
                abs(x - self.start_sprite.center_x) < self.start_sprite.width / 2
                and abs(y - self.start_sprite.center_y) < self.start_sprite.height / 2
        ):
            SecondWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SECOND_WINDOW_TITLE)


def setup_game(width=800, height=600, title="Cross"):
    game = MyGame(width, height, title)
    return game


def main():
    setup_game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()