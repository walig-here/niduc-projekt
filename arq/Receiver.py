# Odbiorca - wersja deweloperska
# - Odbiera wiadomośc od kontrolera odbiorcy
# - Agreguje statystyki na temat przeprowadzonej transmisji
# - Zapisuje statystyki do pliku *.csv
# ========================================================================
# Odbiorca - wersja ostateczna
# - zapisywanie danych o efektywnej przepustowości (bity użyteczne / bity przesłane)
# - zapisywanie danych o łącznej ilości błędów (wykryte + niewykryte)

import csv

import numpy


class Receiver:

    def __init__(self):
        self.error_count = 0
        self.simulation_data = []

    # -----------------------------------------------------------------------
    # Odbiera wiadomość z kontrolera transmisji oraz oryginalną wiadomość
    # od nadawcy.
    #
    # Parametry:
    # received_message - wiadomość bitowa odbierana przez odbiorce
    # original_message - oryginalna wiadomość bitowa wysłana przez nadawce
    # error_count - ilość wykrytych błędów
    #
    # Zwraca:
    # Nic.
    # -----------------------------------------------------------------------
    def receive_message(self, received_message: numpy.array, original_message: numpy.array, error_count: numpy.uint):
        self.simulation_data.append((received_message,
                                     original_message,
                                     error_count,
                                     numpy.count_nonzero(received_message != original_message)
                                     ))

    # -----------------------------------------------------------------------
    # Pobiera informacje na temat wykrytych w czasie transmisji błędów.
    #
    # Parametry:
    #
    # Zwraca:
    # Nic.
    # -----------------------------------------------------------------------
    def set_error_count(self, error_count: numpy.uint):
        self.error_count = error_count

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
            writer.writerow(['Received Message', 'Original Message', 'Detected errors', 'Undetected errors'])
            for received_message, original_message, detected_errors, undetected_errors in self.simulation_data:
                writer.writerow([received_message, original_message, detected_errors, undetected_errors])
