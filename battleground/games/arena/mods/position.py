
from .. import arena_game
from .. import dungeon
from .. import event
from .. import gladiator
from .. import calc

import random


class ArenaGameEngine(arena_game.ArenaGameEngine):

    def __init__(self, state=None, *args, **kwargs):
        """
        :param state: {"dungeon": {"size": int},
                       ...}
        """
        super().__init__(state=state, *args, **kwargs)

    def init_new_gladiator_stats(self, gladiators, *args, **kwargs):
        """
        :param gladiators: list of Gladiators
        :return: list of stats to create Gladiator object at start of the game
        """
        stats = super().init_new_gladiator_stats(gladiators, *args, **kwargs)

        if gladiators:
            size = self.get_dungeon_size(gladiators)
        else:
            size = ((0, 2), (0, 2))
        # find free position
        while True:
            pos = (random.randint(size[0][0], size[0][1]),
                   random.randint(size[1][0], size[1][1]))
            if all(pos != g.pos for g in gladiators):
                break
        stats["pos"] = pos
        return stats

    def init_new_dungeon_stats(self, gladiators, *args, **kwargs):
        """
        :return: list of stats to create Dungeon object at start of the game
        """
        stats = super().init_new_dungeon_stats(gladiators, *args, **kwargs)
        stats["size"] = self.get_dungeon_size(gladiators)
        return stats

    @staticmethod
    def get_dungeon_size(gladiators):
        positions = [g.pos for g in gladiators]
        pos_x = [p[0] for p in positions]
        pos_y = [p[1] for p in positions]
        size = ((min(pos_x) - 1, max(pos_x) + 1),
                (min(pos_y) - 1, max(pos_y) + 1))
        return size

    @staticmethod
    def within_bounds(pos, size):
        return bool(size[0][0] <= pos[0] <= size[0][1]
                    and size[1][0] <= pos[1] <= size[1][1])

    def get_move_options(self, gladiator_index):
        """
        Used by agent to get available moves
        :param gladiator_index: index in gladiators list
        :return: (dict) [{type: name,
                          targets: [{target: target,
                                     values: []
                                     },
                                    ]
                          },
                         ]
        """
        gladiator = self.gladiators[gladiator_index]
        options = super().get_move_options(gladiator_index=gladiator_index)

        # add options for "move"
        directions = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        targets = [d for d in directions
                   if self.within_bounds(calc.add_tuples(gladiator.pos, d),
                                         self.dungeon.size)]
        if targets:
            options_move = {"type": "move",
                            "targets": targets
                            }
            options.append(options_move)

        # add options for "attack"
        # targets are indices of gladiators list
        targets = [self.gladiators.index(g) for g in self.gladiators
                   if (calc.dist(gladiator.pos, g.pos) <= gladiator.range
                       and not g.is_dead()
                       and g is not gladiator)]
        # replace attack option from super()
        index = len(options) - 1
        for option in reversed(options):
            for _, value in option.items():
                if value is "attack":
                    del options[index]
            index -= 1
        if targets:
            options_attack = {"type": "attack",
                              "targets": targets
                              }
            options.append(options_attack)

        return options

    def init_queued_event_stats(self, time, glad_event, move):
        """
        As super(), but adds information about the position at event creation.
        :param time: time the event is created
        :param glad_event: event the gladiator is called
        :param move: move the gladiator wants to queue
        :return: dict of stats for instantiation of event.
        """
        stats = super().init_queued_event_stats(time, glad_event, move)
        glad = self.gladiators[glad_event.owner]
        stats["origin"] = glad.pos
        return stats

    def handle_event(self, event):
        if event.type is "move":
            self.move_move(event)
        else:
            super().handle_event(event=event)

        self.dungeon.shrink_dungeon(self.state)
        return None

    def move_move(self, event):
        """
        Moves owner of event by target vector (if space is free.)
        :param event:
        :return:
        """
        blocked = False
        player = self.gladiators[event.owner]
        # for glad in self.gladiators:
        #     if glad.pos == calc.add_tuples(player.pos, event.target):
        #         blocked = True
        if not blocked:
            player.move(event.target)
        return None


class Dungeon(dungeon.Dungeon):
    def __init__(self, size, *args, **kwargs):
        """
        :param size: ((int, int), (int, int))
        """
        super().__init__(*args, **kwargs)
        self.size = size

    def get_init(self, *args, **kwargs):
        init = super().get_init(*args, **kwargs)
        init["size"] = self.size
        return init

    def shrink_dungeon(self, state):
        # shrink dungeon
        positions = [g.pos for g in state["gladiators"]]
        pos_x = [p[0] for p in positions]
        pos_y = [p[1] for p in positions]
        self.size = ((min(pos_x), max(pos_x)), (min(pos_y), max(pos_y)))
        return None


class Event(event.Event):
    def __init__(self, origin=None, *args, **kwargs):
        """
        :param owner: (int) gladiator index
        :param time_stamp: (float)
        :param type: (str) name of type of event
        :param target: (int) Gladiator index OR (int, int) position
        :param origin: (int, int) position
        """
        super().__init__(*args, **kwargs)
        self.origin = origin

    def get_init(self, *args, **kwargs):
        init = super().get_init(*args, **kwargs)
        init["origin"] = self.origin
        return init


class Gladiator(gladiator.Gladiator):
    def __init__(self, pos=(0, 0), *args, **kwargs):
        """
        :param pos: (int, int)
        """
        super().__init__(*args, **kwargs)
        self.pos = pos
        self.range = 1

    def get_init(self, *args, **kwargs):
        init = super().get_init(*args, **kwargs)
        init["pos"] = self.pos
        init["range"] = self.range
        return init

    def attack(self, target):
        """
        :param target: object that has a position, evasion score and protection tuple
        :return: (int) damage
        """
        pos_o = self.pos
        pos_t = target.pos
        if calc.dist(pos_o, pos_t) > self.range:
            return 0
        else:
            return super().attack(target=target)

    def move(self, direction):
        """
        :param direction: (int, int) direction vector (list)
        :return: None
        """
        self.pos = calc.add_tuples(self.pos, direction)
        return None

    def get_cost(self, type, *args, **kwargs):
        """
        :param type: (str)
        :param target: NotImplemented
        :param value: (int)
        :return: (int) cost in turn counts of a given action, given its target and value.
        """
        if type == "move":
            cost = self.get_speed()
        else:
            cost = super().get_cost(type=type, *args, **kwargs)
        return int(cost)
