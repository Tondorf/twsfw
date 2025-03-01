#!/usr/bin/env python3
import glob
import os
import pathlib
import signal
import time

from twsfw import Game
from twsfw.game import World

RUN = True
FPS = 23.97
S_PER_FRAME = 1 / FPS


def signal_handler(signal, frame):
    print("SIGINT received, but that's OK, I don't hate you!")
    global RUN
    RUN = False


def wasm_agents() -> list[bytes]:
    agents_dir = pathlib.Path(__file__).parents[1] / "agents"
    wasms = glob.glob(os.path.join(agents_dir / "*", "*.wasm"))
    print("Found", len(wasms), "agent files:", wasms)
    agents = [pathlib.Path(w).read_bytes() for w in wasms]
    print("Loaded", len(agents), "agents")
    return agents


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    agents = wasm_agents()
    wörld = World(
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
    game = Game(agents=agents, world=wörld)
    print("Game starting...")

    while RUN:
        start = time.time()

        state = game.tick()
        # print("tick:", game.ticks)
        # w = state.world

        time.sleep(start - time.time() + S_PER_FRAME)
