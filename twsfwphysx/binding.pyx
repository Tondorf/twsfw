from dataclasses import dataclass

from libc.stdint cimport uint32_t, int32_t


cdef extern from "twsfwphysx/twsfwphysx.h":
    cdef struct twsfwphysx_vec:
        float x
        float y
        float z

    cdef struct twsfwphysx_agent:
        twsfwphysx_vec r
        twsfwphysx_vec L
        float a
        int32_t hp

    cdef struct twsfwphysx_agents:
        twsfwphysx_agent *agents
        int32_t size

    cdef struct twsfwphysx_missile:
        twsfwphysx_vec r
        twsfwphysx_vec L

    cdef struct twsfwphysx_missiles:
        twsfwphysx_missile *missiles
        int32_t size
        int32_t capacity

    cdef struct twsfwphysx_world:
        float friction
        float restitution
        float agent_radius
        float missile_acceleration

    const char* twsfwphysx_version()

    twsfwphysx_agents twsfwphysx_create_agents(int32_t size)

    void twsfwphysx_delete_agents(twsfwphysx_agents *agents)

    void twsfwphysx_set_agent(const twsfwphysx_agents *batch,
                              twsfwphysx_agent agent,
                              int32_t index)
    
    twsfwphysx_missiles twsfwphysx_new_missile_batch()

    void twsfwphysx_delete_missile_batch(twsfwphysx_missiles *missiles)

    void twsfwphysx_add_missile(twsfwphysx_missiles *missiles,
                                twsfwphysx_missile missile)
                                
    void *twsfwphysx_create_simulation_buffer()

    void twsfwphysx_delete_simulation_buffer(void *buffer)

    void twsfwphysx_simulate(twsfwphysx_agents *agents,
                             twsfwphysx_missiles *missiles,
                             const twsfwphysx_world *world,
                             float t,
                             int32_t n_steps,
                             void *buffer)


def get_twsfwphysx_version():
    cdef const char* version = twsfwphysx_version()
    return version.decode("utf-8")


@dataclass
class World:
    friction: float
    restitution: float
    agent_radius: float
    missile_acceleration: float


@dataclass
class Vec3:
    x: float
    y: float
    z: float


@dataclass
class Agent:
    r: Vec3
    L: Vec3
    a: float
    hp: int
    

@dataclass
class Missile:
    r: Vec3
    L: Vec3


def make_twsfwphysx_agent(agent: Agent):
    cdef twsfwphysx_vec r = twsfwphysx_vec(agent.r.x, agent.r.y, agent.r.z)
    cdef twsfwphysx_vec L = twsfwphysx_vec(agent.L.x, agent.L.y, agent.L.z)
    return twsfwphysx_agent(r, L, agent.a, agent.hp)


def make_twsfwphysx_missile(missile: Missile):
    cdef twsfwphysx_vec r = twsfwphysx_vec(missile.r.x, missile.r.y, missile.r.z)
    cdef twsfwphysx_vec L = twsfwphysx_vec(missile.L.x, missile.L.y, missile.L.z)
    return twsfwphysx_missile(r, L)


cdef class Engine():
    cdef twsfwphysx_world _world
    cdef twsfwphysx_agents _agents
    cdef twsfwphysx_missiles _missiles
    cdef void *_simulation_buffer

    def __init__(self, world: World, agents: list[Agent]):
        self._world = twsfwphysx_world(
            world.friction,
            world.restitution,
            world.agent_radius,
            world.missile_acceleration
        )

        self._agents = twsfwphysx_create_agents(len(agents))
        for i, agent in enumerate(agents):
            twsfwphysx_set_agent(&self._agents, make_twsfwphysx_agent(agent), i)

        self._missiles = twsfwphysx_new_missile_batch()

        self._simulation_buffer = twsfwphysx_create_simulation_buffer()

    def __del__(self):
        twsfwphysx_delete_agents(&self._agents)
        twsfwphysx_delete_missile_batch(&self._missiles)

        if self._simulation_buffer:
            twsfwphysx_delete_simulation_buffer(self._simulation_buffer)

    def simulate(self, *, t: float, n_steps: int):
        twsfwphysx_simulate(
            &self._agents,
            &self._missiles,
            &self._world,
            t,
            n_steps,
            self._simulation_buffer
        )

    def add_missile(self, missile: Missile):
        twsfwphysx_add_missile(&self._missiles, make_twsfwphysx_missile(missile))

    @property
    def agents(self):
        agents = [self._agents.agents[i] for i in range(self._agents.size)]
        return [Agent(
            Vec3(a["r"]["x"], a["r"]["y"], a["r"]["z"]),
            Vec3(a["L"]["x"], a["L"]["y"], a["L"]["z"]),
            a["a"],
            a["hp"],
        ) for a in agents]

    @property
    def missiles(self):
        missiles = [self._missiles.missiles[i] for i in range(self._missiles.size)]
        return [Missile(
            Vec3(m["r"]["x"], m["r"]["y"], m["r"]["z"]),
            Vec3(m["L"]["x"], m["L"]["y"], m["L"]["z"]),
        ) for m in missiles]
        
