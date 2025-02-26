import logging
import math
import struct
from dataclasses import dataclass

import wasmtime

from twsfw import physx

logger = logging.getLogger(__name__)


@dataclass
class WASMAgent:
    instance: wasmtime.Instance
    memory: wasmtime.Memory
    func: wasmtime.Func


@dataclass
class World(physx.World):
    dt: float
    n_simulation_steps: int
    max_hp: float
    healing_rate: float
    max_rotation_rate: float
    max_agent_acceleration: float


@dataclass
class State:
    agents: list[physx.Agent]
    missiles: list[physx.Missile]
    world: physx.World

    def serialize(self) -> tuple[bytes, dict[str, int]]:
        buffer = b""

        agents_ptr = 0
        buffer += b"".join(agent.serialize() for agent in self.agents)

        missiles_ptr = len(buffer)
        buffer += b"".join(missile.serialize() for missile in self.missiles)

        world_ptr = len(buffer)
        buffer += self.world.serialize()

        return buffer, dict(agents=agents_ptr, missiles=missiles_ptr, world=world_ptr)


def init_agents(n, *, init_hp):
    agents = []
    for i in range(n):
        angle = 2.0 * math.pi * i / n
        r = physx.Vec3(math.cos(angle), math.sin(angle), 0.0)
        u = physx.Vec3(0.0, 0.0, 1.0)
        agents.append(physx.Agent(r, u, v=0.0, a=0.0, hp=init_hp))

    return agents


class Game:
    def __init__(self, *, agents: list[str], world: World):
        self.physx_engine = physx.Engine(
            world, init_agents(len(agents), init_hp=world.max_hp)
        )
        self.state = State(self.physx_engine.agents, self.physx_engine.missiles, world)

        self.wasm_engine = wasmtime.Engine()
        self.wasm_store = wasmtime.Store(self.wasm_engine)
        self.wasm_agents = []

        for agent in agents:
            module = wasmtime.Module(self.wasm_engine, agent)
            instance = wasmtime.Instance(self.wasm_store, module, [])
            memory = instance.exports(self.wasm_store)["memory"]
            func = instance.exports(self.wasm_store)["twsfw_agent_act"]

            self.wasm_agents.append(WASMAgent(instance, memory, func))

    def _call_agents(self):
        buffer, offset = self.state.serialize()

        offset["action"] = len(buffer)
        buffer += b"\x00\x00\x00\x00"

        for agent in self.wasm_agents:
            agent.memory.write(self.wasm_store, buffer)
            value = agent.func(
                self.wasm_store,
                offset["agents"],
                len(self.state.agents),
                offset["missiles"],
                len(self.state.missiles),
                offset["world"],
                0,
                offset["action"],
            )

            (action_type,) = struct.unpack(
                "<i",
                agent.memory.read(
                    self.wasm_store, offset["action"], offset["action"] + 4
                ),
            )

            yield action_type, value

    def tick(self):
        for i, agent in enumerate(self.state.agents):
            hp = min(agent.hp + self.state.world.healing_rate, self.state.world.max_hp)
            self.physx_engine.update_agent(agent_idx=i, hp=hp)

        self.physx_engine.simulate(
            t=self.state.world.dt, n_steps=self.state.world.n_simulation_steps
        )

        self.state.agents = self.physx_engine.agents
        self.state.missiles = self.physx_engine.missiles

        for i, (action_type, value) in enumerate(self._call_agents()):
            match action_type:
                case 0:  # turn
                    max_angle = self.state.world.max_rotation_rate
                    self.physx_engine.rotate_agent(
                        agent_idx=i,
                        angle=min(max(value, -max_angle), max_angle),
                        degrees=True,
                    )

                case 1:  # change acceleration
                    max_a = self.state.world.max_agent_acceleration
                    self.physx_engine.update_agent(
                        agent_idx=i, a=min(max(value, 0.0), max_a)
                    )

                case 2:  # fire
                    self.physx_engine.launch_missile(agent_idx=i)

                case _:
                    logger.info("Unknown action from agent %d", i)

        return self.state
