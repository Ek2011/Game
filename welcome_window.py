import arcade
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Cross"


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.GRAY)

        # Текстовый объект
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

        self.tennisist_sprite_1 = arcade.Sprite("C:/Users/star/Desktop/проект Arcade/welcome/tennisist.png", scale=0.35)
        self.tennisist_sprite_1.center_x = SCREEN_WIDTH // 3
        self.tennisist_sprite_1.center_y = 300
        self.all_sprites.append(self.tennisist_sprite_1)

        self.tennisist_sprite_2 = arcade.Sprite("C:/Users/star/Desktop/проект Arcade/welcome/tenn3.png", scale=0.2)
        self.tennisist_sprite_2.center_x = SCREEN_WIDTH - 150
        self.tennisist_sprite_2.center_y = 100
        self.all_sprites.append(self.tennisist_sprite_2)

        self.start_sprite = arcade.Sprite("C:/Users/star/Desktop/проект Arcade/welcome/startbutton.png", scale=0.3)
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


def setup_game(width=800, height=600, title="Cross"):
    game = MyGame(width, height, title)
    return game


def main():
    setup_game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()