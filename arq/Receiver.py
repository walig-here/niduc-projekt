# Odbiorca - wersja deweloperska
# - Odbiera wiadomośc od kontrolera odbiorcy
# - Agreguje statystyki na temat przeprowadzonej transmisji
# - Zapisuje statystyki do pliku *.csv

import csv

import numpy


class Receiver:

    def __init__(self):
        self.error_count = 0
        self.received_messages = []
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
        self.received_messages.append((received_message, original_message))
        errors = numpy.sum(received_message != original_message)
        self.set_error_count(errors)

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
        self.error_count += error_count

    # -----------------------------------------------------------------------
    # Zapisuje statystyki do pliku *.csv
    #
    # Parametry:
    # file_name - nazwa pliku, do którego zapisane zostaną statystyki
    #
    # Zwraca:
    # Nic.
    # -----------------------------------------------------------------------
    def save_statistics(self, file_name: str):
        with open(file_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Received Message', 'Original Message'])
            for received_message, original_message in self.received_messages:
                writer.writerow([received_message, original_message])
