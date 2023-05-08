import os

import numpy
from arq import ARQ as SimulationModule

# PARAMETRY SYMULACJI
error_probability = 0.001  # prawdopodobieństwo przekłamania bitu
message_length = 256       # długość wiadomości
segment_length = 32         # długość segmentów

turns = 1000                # ilość powtórzeń symulacji
file_name = "stats"         # nazwa pliku wyjściowego


def main():

    if message_length%segment_length != 0:
        print("Zadano nieprawidłową długość semgnetu!")
        return

    print("\nRozpoczynam symulacje...")
    arq_system = SimulationModule.ARQ(message_length, turns, file_name)
    for i in range(0, turns):

        if i % (turns*0.05) == 0:
            print(str(i/(turns*0.05)*5)+"%\t("+str(i)+"/"+str(turns)+")")

        arq_system.simulate_transmission(message_length, segment_length)
    arq_system.save_results(file_name)

    os.system('cls')
    print("Zapisano", turns, "wyników do", file_name+".csv")


if __name__ == "__main__":
    main()
