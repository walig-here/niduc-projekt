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
    def __init__(self):
        self.ack = True
    
    def push_segment(self, segment: numpy.array):
        if self.ack:
            self.segment = segment
            self.ack = False

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
        self.ack = response

    # -----------------------------------------------------------------------
    # Wyciąga segment bitowy z kontrolera.
    #
    # Zwraca:
    # Segment bitowy z pamięci kontrolera.
    # -----------------------------------------------------------------------
    def pop_segment(self) -> numpy.array:
        return self.segment