# Kontroler nadawcy
# - Przezysła segment do kanału
# - Pobiera segment z kodera
# - Odbiera wiadomości z kanału zwrotnego


import numpy


class SenderController:
    # -----------------------------------------------------------------------
    # Wprowadza segment bitowy do kontrolera.
    #
    # Parametry:
    # segment - segment bitowy wchodzący do kontrolera
    #
    # Zwraca:
    # Nic.
    # -----------------------------------------------------------------------
    def push_segment(self, segment: numpy.array):
        return

    # -----------------------------------------------------------------------
    # Wprowadza do kontrolera odpowiedź z kanału zwrotnego.
    #
    # Parametry:
    # response - wiadomość z kanału zwrotnego
    #
    # Zwraca:
    # Nic
    # -----------------------------------------------------------------------
    def push_response(self, response: bool):
        return

    # -----------------------------------------------------------------------
    # Wyciąga segment bitowy z kontrolera.
    #
    # Zwraca:
    # Segment bitowy z pamięci kontrolera.
    # -----------------------------------------------------------------------
    def pop_segment(self) -> numpy.array:
        return numpy.array(0)