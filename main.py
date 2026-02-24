from agentes.drone_agent import DroneAgent
from env.drone_environment import DroneEnvironment

def main():

    env = DroneEnvironment(
        width=10,
        height=10,
        deliveries=[(3, 3), (7, 2)],
        obstacles=[(5, 5)]
    )

    agent = DroneAgent(env)

    env.add_agent(agent)

    # CORRETO:
    env.run(steps=1000)


if __name__ == "__main__":
    main()