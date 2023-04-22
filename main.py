import os

import numpy
from arq import ARQ as SimulationModule

# PARAMETRY SYMULACJI
error_probability = 0.001  # prawdopodobieństwo przekłamania bitu
message_length = 128       # długość wiadomości
segment_length = 4         # długość segmentów

turns = 1000                # ilość powtórzeń symulacji
file_name = "stats"         # nazwa pliku wyjściowego

def main():

    if message_length%segment_length != 0:
        print("Zadano nieprawidłową długość semgnetu!")
        return

    print("\nRozpoczynam symulacje...")
    arq_system = SimulationModule.ARQ(error_probability, segment_length)
    for i in range(0, turns):

        if i % (turns*0.05) == 0:
            print(str(i/(turns*0.05)*5)+"%\t("+str(i)+"/"+str(turns)+")")

        arq_system.simulate_transmission(message_length, segment_length)
    arq_system.save_results(file_name)

    os.system('cls')
    print_parameters()
    print("Zapisano", turns, "wyników do", file_name+".csv")

# Główna pętla symulująca całą drogę wiadomości


def print_parameters():
    print("\nPARAMETRY SYMULACJI:")
    print("Długość wiadomości:", message_length, "bitów")
    print("Długość segmentu:", segment_length, "bitów")
    print("Prawdopodobieństwo przekłamania bitu:", str(error_probability*100)+"%")

if __name__ == "__main__":
    main()
