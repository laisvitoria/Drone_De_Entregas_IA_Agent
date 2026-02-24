from env.drone_environment import DroneEnvironment
from agentes.drone_agent import DroneAgent

def main():
    width = 5
    height = 5

    deliveries = [(4, 3)]

    obstacles = [
        (1, 1),
        (2, 1),
        (1, 3)
    ]

    recharge_points = [(2, 2)]

    env = DroneEnvironment(
        width,
        height,
        deliveries,
        obstacles,
        recharge_points
    )

    agent = DroneAgent(env)

    env.add_agent(agent)

    env.run(steps=50)


if __name__ == "__main__":
    main()