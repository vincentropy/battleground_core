# from battleground.game_runner import GameRunner

# from games.arena import calc

from battleground.games.arena.arena_game import ArenaGameEngine
from battleground.games.arena.dungeon import Dungeon
from battleground.games.arena.gladiator import Gladiator
from battleground.games.arena.arena_agent import ArenaAgent

import random


def test_engine():
    age = ArenaGameEngine(num_players=2)
    # assert age.get_game_name() == "Arena"
    assert isinstance(age.gladiators, list)
    assert isinstance(age.dungeon, Dungeon)
    assert isinstance(age.event_queue, list)
    state = age.get_state()
    assert isinstance(state, dict)
    assert "gladiators" in state
    assert "dungeon" in state
    assert "queue" in state
    assert "scores" in state
    assert "move_options" in state
    assert isinstance(age.get_current_player(), int)
    assert isinstance(age.game_over(), bool)


def test_dungeon():
    dungeon = Dungeon()
    assert isinstance(dungeon.get_init(), dict)


def test_gladiator():
    glad = Gladiator()
    assert isinstance(glad.name, str)
    assert isinstance(glad.get_init(), dict)
    assert isinstance(glad.get_stats(), dict)
    assert isinstance(glad.get_skills(), dict)
    assert isinstance(glad.get_accuracy(), int)
    assert isinstance(glad.get_evasion(), int)
    assert isinstance(glad.get_base_damage(), int)
    assert isinstance(glad.get_base_protection(), int)
    assert isinstance(glad.get_damage(), int)
    assert isinstance(glad.get_protection(), int)
    assert isinstance(glad.get_max_hp(), int)
    assert isinstance(glad.max_hp, int)
    assert isinstance(glad.cur_hp, int)
    assert isinstance(glad.is_dead(), bool)
    assert 0 < glad.get_speed()

    options = {"stay": {None: 0},
               "attack": {0: None}
               }
    for action, targets in options.items():
        for target, value in targets.items():
            assert isinstance(glad.get_cost(action, target, value), int)
    stats = {"str": random.randint(1, 3),
             "dex": random.randint(1, 3),
             "con": random.randint(1, 3)}
    skills = {"acc": random.randint(1, 3),
              "eva": random.randint(1, 3),
              "spd": random.randint(1, 3)}
    name = "Maximus"
    team = random.randint(1, 10)
    vlad = Gladiator(stats=stats, skills=skills,
                     name=name, team=team, cur_hp=1, cur_sp=1)
    assert vlad.name == name
    assert vlad.team == team
    assert vlad.base_stats == stats
    assert vlad.base_skills == skills
    assert vlad.cur_hp == 1
    assert isinstance(vlad.attack(glad), int)


def test_player():
    age = ArenaGameEngine(num_players=3, type="Pit")
    state = age.get_state()
    current_player = age.get_current_player()
    options = age.get_move_options(current_player)
    agent = ArenaAgent()
    move = agent.move(state)
    assert "type" in move
    type = move["type"]
    if "tool" in move:
        tool = move["tool"]
    if "target" in move:
        target = move["target"]
    if "value" in move:
        value = move["value"]

    types = [option["type"] for option in options]
    assert type in types
    # check that move in options:
    # for option in options:
    #     if option["type"] is type:
    #         if "tools" in option:
    #             options = option["tools"]
    #             if isinstance(options, list):
    #                 tools = [tool_option["tool"] for tool_option in options]
    #                 assert tool in tools
    #                 for option in options:
    #                     if option["tool"] is tool:


def test_game():
    assert True


if __name__ == "__main__":
    test_engine()
    test_dungeon()
    test_gladiator()
    test_player()
    test_game()
