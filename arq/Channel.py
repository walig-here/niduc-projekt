# Kanał transmisyjny - wersja deweloperska
# - Odbiera segmenty
# - Przekłamuje bity z pewnym prawdopodobieństwem


import numpy


class Channel:
    #-----------------------------------------------------------------------
    # Wprowadza segment bitowy do kanału.
    #
    # Parametry:
    # segment - segment bitowy wchodzący do kanału
    #
    # Zwraca:
    # Nic.
    #-----------------------------------------------------------------------
    def send_segment(self, segment: numpy.array):
        return

    # -----------------------------------------------------------------------
    # Wyciąga segment bitowy z kanału.
    #
    # Zwraca:
    # Segment bitowy znajduący się w kanale.
    # -----------------------------------------------------------------------
    def recieve_segment(self) -> numpy.array:
        return numpy.array(0)
