# Koder - wersja deweloperska
# - Segmentuje wiadomość
# - Dokłada do segmentów narzut związany z kodowaniem
# - Przekazuje segmenty do kontrolera transmisji nadawcy


import numpy


class Encoder:
    # -----------------------------------------------------------------------
    # Wprowadza wiadomość bitową do kodera.
    #
    # Parametry:
    # message - wiadomość bitowa wchodząca do kodera
    #
    # Zwraca:
    # Nic.
    # -----------------------------------------------------------------------
    def push_message(self, message: numpy.array):
        return

    # -----------------------------------------------------------------------
    # Wyciąga kolejny segment bitowy znajdujący się w pamięci kodera.
    #
    # Zwraca:
    # Kolejny segment segment bitowy z pamięci kodera.
    # -----------------------------------------------------------------------
    def pop_segment(self) -> numpy.array:
        return numpy.array(0)
