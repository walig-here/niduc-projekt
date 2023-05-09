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
    def receive_message(self, received_message: numpy.array, original_message: numpy.array, error_count: numpy.uint, total_sent_bits: int, retransmissions: int):
        self.simulation_data.append((
            error_count,
            numpy.count_nonzero(received_message != original_message),
            (len(received_message))/total_sent_bits,
            retransmissions
        ))

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
            writer.writerow(['Bledy', 'Wykryte bledy', 'Niewykryte bledy', 'Efektywna przepustowosc', 'Ilosc retransmisji'])
            for detected_errors, undetected_errors, throughtput, retransmissions in self.simulation_data:
                writer.writerow([detected_errors + undetected_errors,
                                 detected_errors,
                                 undetected_errors,
                                 throughtput,
                                 retransmissions
                                ])
