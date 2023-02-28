import pygame
import pygame_menu

from scorched_earth import game_constants
from scorched_earth import game_core


class ScorchedEarthMenu(object):
    def __init__(self, screen, clock):
        super()
        self.screen = screen
        self.clock = clock
        self.color = [game_constants.BLUE, game_constants.RED]
        self.init_menu()

    def init_menu(self):
        self.main_menu = pygame_menu.Menu(
            width=game_constants.SCREEN_WIDTH * 0.75,
            height=game_constants.SCREEN_HEIGHT * 0.7,
            title='Scorched Earth Remastered',
            theme=pygame_menu.themes.THEME_BLUE,
        )
        self.options_menu = pygame_menu.Menu(
            width=game_constants.SCREEN_WIDTH * 0.75,
            height=game_constants.SCREEN_HEIGHT * 0.7,
            title='Options Menu',
        )

        self.options_menu.add.selector(
            'Wind', [('Off', False), ('On', True)], onchange=self._enable_wind
        )
        self.options_menu.add.selector(
            'Gravity',
            [
                ('Earth', 9.8),
                ('Moon', 1.6),
                ('Mars', 3.7),
                ('SuperEarth', 19.6),
            ],
            onchange=self._set_gravity,
        )
        self.options_menu.add.selector(
            'RandomEdges',
            [('Off', False), ('On', True)],
            onchange=self._set_edges_behaviour,
        )
        self.options_menu.add.color_input(
            'Tank1: ',
            color_type='rgb',
            input_separator='-',
            default=game_constants.BLUE,
            onreturn=self._change_color_1,
        )
        self.options_menu.add.color_input(
            'Tank2: ',
            color_type='rgb',
            input_separator='-',
            default=game_constants.RED,
            onreturn=self._change_color_2,
        )
        self.options_menu.add.vertical_margin(10)
        self.options_menu.add.button(
            'Return to Main Menu',
            pygame_menu.events.BACK,
            align=pygame_menu.locals.ALIGN_CENTER,
        )

        self.main_menu.add.button('Play', self._start_playing, self.color)
        self.main_menu.add.button('Options', self.options_menu)
        self.main_menu.add.vertical_margin(10)
        self.main_menu.add.button('Quit', pygame_menu.events.EXIT)

    # TODO(lajoskatona): it's not that dynamic or scale well....
    def _change_color_1(self, selected_color):
        print('change color 1: ', selected_color)
        self.color[0] = selected_color

    def _change_color_2(self, selected_color):
        print('change color 2: ', selected_color)
        self.color[1] = selected_color

    def _enable_wind(self, value, enable):
        print('_enable_wind: %s  (%s)' % (value, enable))

    def _set_gravity(self, value, gravity):
        print(f'_set_gravity: {value} ({gravity})')

    def _set_edges_behaviour(self, value, edge_behaviour):
        print(f'_set_edges_behaviour: {value} ({edge_behaviour})')

    def _start_playing(self, *args, **kwargs):
        print(args)
        print(kwargs)
        self.main_menu.disable()
        self.main_menu.full_reset()
        game = game_core.Game(self.screen, self.clock, self.color)
        game.game_loop()

    def menu_loop(self):
        while True:
            if self.main_menu.is_enabled():
                self.main_menu.mainloop(
                    self.screen, fps_limit=game_constants.BASE_TICK
                )
                self.clock.tick(game_constants.BASE_TICK)
                pygame.display.flip()
