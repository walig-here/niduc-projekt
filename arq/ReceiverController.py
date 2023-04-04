# Kontroler odbiorcy - wersja deweloperska
# - Wysyła żądania retransmisji lub potwierdzenia odbioru
# - Przekazuje wiadomość odbiorcy
# - Scala otrzymane segmenty w wiadomość


import numpy

from arq import Receiver


class ReceiverController:

    def __init__(self, receiver: Receiver):
        self.receiver = receiver
        self.messages_queue = []
        self.responses_queue = []

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
        self.messages_queue.append(message)

    # -----------------------------------------------------------------------
    # Wyciąga z kontrolera odpowiedź, która ma zostać przesłana kanałem
    # zwrotnym.
    #
    # Zwraca:
    # Wiadomość zwrotną kotnrolera. True, gdy jest to potwierdzenie odbioru.
    # False, gdy jest to żądanie retransmisji.
    # -----------------------------------------------------------------------
    def pop_response(self) -> bool:
        if not self.responses_queue:
            return None
        return self.responses_queue.pop(0)

    # -----------------------------------------------------------------------
    # Wyciąga wiadomość bitową z kontrolera.
    #
    # Zwraca:
    # Wiadomość bitową z pamięci kontrolera.
    # -----------------------------------------------------------------------
    def pop_message(self) -> numpy.array:
        if not self.messages_queue:
            return None
        return self.messages_queue.pop(0)

    # -----------------------------------------------------------------------
    # Przetwarza otrzymane wiadomości, sprawdza błędy i generuje odpowiedzi.
    #
    # Zwraca:
    # Nic.
    # -----------------------------------------------------------------------

    def process_messages(self):
        while self.messages_queue:
            message = self.messages_queue.pop(0)
            original_message = self.decode_message(message)
            self.receiver.receive_message(message, original_message)
            self.responses_queue.append(self.check_errors(message, original_message))

    # -----------------------------------------------------------------------
    # Sprawdza, czy wystąpiły błędy w otrzymanej wiadomości, porównując ją
    # z oryginalną wiadomością.
    #
    # Parametry:
    # received_message - wiadomość bitowa otrzymana przez odbiorcę
    # original_message - oryginalna wiadomość bitowa wysłana przez nadawcę
    #
    # Zwraca:
    # True, gdy otrzymana wiadomość jest równa oryginalnej wiadomości.
    # False, gdy wystąpiły błędy.
    # ----------------------------------------------------------------------
    def check_errors(self, received_message: numpy.array, original_message: numpy.array) -> bool:
        return numpy.array_equal(received_message, original_message)

    # -----------------------------------------------------------------------
    # Dekoduje wiadomość przy użycciu kodów BCH.
    # #
    # # Parametry:
    # # message - wiadomość bitowa do zdekodowania
    # #
    # # Zwraca:
    # # Oryginalną wiadomość bitową po dekodowaniu.
    # # -----------------------------------------------------------------------

    def decode_message(self, message:numpy.array) -> numpy.array:
        #implementacja dekodowania wiadomości przy użyciu kodów BCH
        return numpy.array(0)
