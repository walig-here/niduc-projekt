# Źródło - wersja deweloperska
# - generuje losową wiadomość bitową
#========================================================================
# DONE!

import numpy


class Source:
    # -----------------------------------------------------------------------
    # Wyciąga ze źródła wiadomośc bitową.
    #
    # Zwraca:
    # Wiadomość bitową znajdującą się w źródle.
    # -----------------------------------------------------------------------
    def pop_message(self, message_length: int) -> numpy.array:
        return self.generate_random_bits_message(message_length)
    

    def generate_random_bits_message(self, length: int) -> numpy.array:
        bits = numpy.random.choice([0, 1], size=length)
        return bits
    
    def generate_random_bytes_message(self, length: int) -> numpy.array:
        bytes = numpy.zeros((length, 8), dtype=int)
        for i in range(length):
            bytes[i] = numpy.random.choice([0, 1], size=8)
        return bytes

        