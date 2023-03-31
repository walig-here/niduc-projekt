# Kontroler odbiorcy - wersja deweloperska
# - Wysyła żądania retransmisji lub potwierdzenia odbioru
# - Przekazuje wiadomość odbiorcy


import numpy


class ReceiverController:
    # -----------------------------------------------------------------------
    # Wprowadza wiadomość bitową do kontrolera.
    #
    # Parametry:
    # message - wiadomość bitowa wchodząca do kontrolera
    #
    # Zwraca:
    # Nic.
    # -----------------------------------------------------------------------
    def push_message(self, message: numpy.array):
        return

    # -----------------------------------------------------------------------
    # Wyciąga z kontrolera odpowiedź, która ma zostać przesłana kanałem
    # zwrotnym.
    #
    # Zwraca:
    # Wiadomość zwrotną kotnrolera. True, gdy jest to potwierdzenie odbioru.
    # False, gdy jest to żądanie retransmisji.
    # -----------------------------------------------------------------------
    def pop_response(self) -> bool:
        return True

    # -----------------------------------------------------------------------
    # Wyciąga wiadomość bitową z kontrolera.
    #
    # Zwraca:
    # Wiadomość bitową z pamięci kontrolera.
    # -----------------------------------------------------------------------
    def pop_message(self) -> numpy.array:
        return numpy.array(0)

