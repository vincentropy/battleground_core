from battleground.game_runner import GameRunner

from games.arena.arena import ArenaGameEngine
from games.arena.arena_game_east import EASTArenaGameEngine
from games.arena.arena_game_eq import EQArenaGameEngine
from games.arena.dungeon import Dungeon
from games.arena.gladiator import Gladiator
from games.arena import arena_agent

from collections import deque
import random


def test_engine():
    age = ArenaGameEngine(num_players=2, type="Arena_1", size=[20, 20])
    assert age.get_game_name() == "Arena_1"
    assert isinstance(age.gladiators, dict)
    assert len(age.gladiators) == 2
    assert isinstance(age.dungeon, Dungeon)


def test_EAST_engine():
    age = EASTArenaGameEngine(num_players=2, type="Arena_1", size=[20, 20])
    assert True


def test_EQ_engine():
    age = EQArenaGameEngine(num_players=2, type="Arena_1", size=[20, 20])
    assert isinstance(age.event_queue, deque)


def test_dungeon():
    size = [random.randint(1, 20), random.randint(1, 20)]
    dun = Dungeon(size)
    assert dun.size == size
    assert isinstance(dun.world, list)
    assert len(dun.world) == size[0]


def test_gladiator():
    pos = [random.randint(1, 100), random.randint(1, 100)]
    team = random.randint(1, 10)
    stats = {"str": random.randint(1, 3),
             "dex": random.randint(1, 3),
             "con": random.randint(1, 3)}
    skills = {"melee": random.randint(1, 3),
              "eva": random.randint(1, 3),
              "speed": random.randint(1, 3)}
    glad = Gladiator(pos=pos, name="Maximus", team=team, stats=stats, skills=skills)
    assert isinstance(glad.pos, list)
    assert glad.pos == pos
    assert glad.name == "Maximus"
    assert glad.team == team
    assert glad.base_stats == stats
    assert glad.base_skills == skills
    assert isinstance(glad.get_stats(), dict)
    assert isinstance(glad.get_skills(), dict)
    assert isinstance(glad.get_attack(), int)
    assert isinstance(glad.get_evasion(), int)
    assert isinstance(glad.get_damage(), list)
    assert isinstance(glad.get_protection(), list)
    assert isinstance(glad.get_max_hp(), int)
    assert isinstance(glad.max_hp, int)
    assert isinstance(glad.cur_hp, int)
    assert isinstance(glad.get_max_sp(), int)
    assert isinstance(glad.max_sp, int)
    assert isinstance(glad.cur_sp, int)
    assert 0 < glad.get_speed()
    assert isinstance(glad.boosts, dict)
    assert glad.set_boosts({"speed": random.randint(1, 3)}) is None
    assert glad.boosts["speed"] > 0
    assert glad.move([1, 2]) is None


def test_player():
    assert True


def test_game():
    assert True


if __name__ == "__main__":
    test_engine()
    test_dungeon()
    test_gladiator()
    test_player()
    test_game()
