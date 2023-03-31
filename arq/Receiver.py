# Odbiorca - wersja deweloperska
# - Odbiera wiadomośc od kontrolera odbiorcy
# - Agreguje statystyki na temat przeprowadzonej transmisji
# - Zapisuje statystyki do pliku *.csv


import numpy


class Receiver:
    # -----------------------------------------------------------------------
    # Odbiera wiadomość z kontrolera transmisji oraz oryginalną wiadomość
    # od nadawcy.
    #
    # Parametry:
    # received_message - wiadomość bitowa odbierana przez odbiorce
    # original_message - oryginalna wiadomość bitowa wysłana przez nadawce
    #
    # Zwraca:
    # Nic.
    # -----------------------------------------------------------------------
    def receive_message(self, received_message: numpy.array, original_message: numpy.array):
        return

    # -----------------------------------------------------------------------
    # Pobiera informacje na temat wykrytych w czasie transmisji błędów.
    #
    # Parametry:
    # error_count - ilość wykrytych błędów
    #
    # Zwraca:
    # Nic.
    # -----------------------------------------------------------------------
    def set_error_count(self, error_count: numpy.uint):
        return
