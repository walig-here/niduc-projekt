import os

import numpy
from arq import ARQ as SimulationModule
from arq import Configuration as Conf


def main():
    turns, file_name, message_length = Conf.configure_simulation()

    print("\nRozpoczynam symulacje...")
    arq_system = SimulationModule.ARQ()
    for i in range(0, turns):

        if i % (turns*0.05) == 0:
            print(str(i/(turns*0.05)*5)+"%\t("+str(i)+"/"+str(turns)+")")

        arq_system.simulate_transmission(message_length)
    arq_system.save_results(file_name)

    os.system('cls')
    print("Zapisano", turns, "wyników do", file_name+".csv")


if __name__ == "__main__":
    main()
