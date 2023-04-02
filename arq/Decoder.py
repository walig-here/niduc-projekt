# Dekoder - wersja deweloperska
# - Wykrywa błędy w odebranych segmentach.
# - Pozbywa się narzutu z otrzymanej wiadomości.
import numpy
import arq.exceptions.VectorError as verr
import arq.exceptions.MemoryError as merr
import komm


class Decoder:
    def __init__(self, segment_length: int):
        self.__received_segment = numpy.array([])
        self.__decoded_segment = numpy.array([])
        self.__decoding_machine = komm.SingleParityCheckCode(segment_length)

    def decode_segment(self) -> bool:
        """
        Dekoduje otrzymany segment i zapisuje odkodowany ciąg w pamięci dekodera.

        :raises MemoryError: przy próbie dekodowania, gdy w pamięci dekodera nie ma segmentu
        :return: True, gdy segment jest poprawny. False, gdy jest niepoprawny.
        """

        if len(self.__received_segment) == 0:
            raise merr.MemoryError("brak segmentu do zdekodowania", merr.MemoryErrorCodes.ELEMENT_NOT_EXIST)

        if len(self.__received_segment) != self.__decoding_machine.length:
            return False

        checksum = self.__received_segment.sum()
        if checksum % 2 == 1:
            return False

        self.__decoded_segment = self.__decoding_machine.decode(self.__received_segment)
        return True

    def decoded_segment(self):
        return self.__decoded_segment

    def push_segment(self, segment: numpy.array):
        """
        Wprowadza segment do dekodera. Przeprowadza kontrolę poprawności
        wprowadzanego segmentu. Nie dopuszcza do wprowadzenia nowego segmentu, gdy w kanale
        znajduje się juz jakiś segment.

        :param segment: wprowadzany do dekodera semgnet
        :raises VectorError: gdy podano wektor niebitowy lub pusty.
        """

        if len(self.__received_segment) != 0:
            raise merr.MemoryError("dekoder zajety", merr.MemoryErrorCodes.OCCUPIED)
        if len(segment) == 0:
            raise verr.VectorError("segment pusty", verr.VectorErrorCodes.EMPTY)
        if not numpy.all(numpy.logical_or(segment == 0, segment == 1)):
            raise verr.VectorError("wektor nie jest binarny", verr.VectorErrorCodes.NON_BINARY)

        self.__received_segment = segment

    def segment(self):
        """
        WŁĄCZNIE NA POTRZEBY TESTÓW JEDNOSTKOWYCH!

        Pobiera segment z dekodera.

        :return: Segment przetwarzany przez dekoder.
        """

        return self.__received_segment

    # -----------------------------------------------------------------------
    # Wyciąga wiadomość bitową z dekodera.
    #
    # Zwraca:
    # Segment bitowy znajduący się w dekoderze.
    # -----------------------------------------------------------------------
    def pop_segment(self) -> numpy.array:
        """
        Wyciąga odkodowany segment z dekodera. Usuwa go przy tym
        z pamięci dekodera.

        :return: Odkodowany segment.
        """

        self.__received_segment = numpy.array([])
        return self.__decoded_segment
