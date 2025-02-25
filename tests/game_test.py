from twsfw import Game
from twsfw.game import World


def test_game(wasm_agent):
    world = World(
        friction=1.0,
        restitution=0.5,
        agent_radius=0.1,
        missile_acceleration=3.0,
        dt=1.0,
        n_simulation_steps=100,
        init_hp=4,
        max_hp=4,
        healing_rate=2,
        max_rotation_rate=5.0,
        max_agent_acceleration=1.0,
    )

    game = Game(agents=[wasm_agent], world=world)
    for _ in range(10):
        state = game.tick()

    assert len(state.agents) == 1
