import pytest

from twsfw import Game
from twsfw.game import World


def test_game(wasm_agent):
    world = World(
        restitution=0.5,
        agent_radius=0.1,
        missile_acceleration=3.0,
        dt=1.0,
        n_simulation_steps=100,
        max_hp=4,
        healing_rate=2,
        max_rotation_rate=5.0,
        max_agent_acceleration=1.0,
    )

    game = Game(agents=[wasm_agent], world=world)
    for _ in range(10):
        state = game.tick()

    w = state.world
    assert w.restitution == pytest.approx(world.restitution)
    assert w.agent_radius == pytest.approx(world.agent_radius)
    assert w.missile_acceleration == pytest.approx(world.missile_acceleration)
    assert w.dt == pytest.approx(world.dt)
    assert w.n_simulation_steps == world.n_simulation_steps
    assert w.max_hp == world.max_hp
    assert w.healing_rate == world.healing_rate
    assert w.max_rotation_rate == pytest.approx(world.max_rotation_rate)
    assert w.max_agent_acceleration == pytest.approx(world.max_agent_acceleration)
    assert len(state.agents) == 1
