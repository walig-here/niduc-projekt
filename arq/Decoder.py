# Dekoder - wersja deweloperska
# - Wykrywa błędy w odebranych segmentach.
# - Pozbywa się narzutu z otrzymanej wiadomości.
# ========================================================================
# Dekoder - wersja ultimate
# - kody cykliczne
# - kody BCH
# - kody Hamminga
# - kody z powieleniem bitu

import numpy
import arq.exceptions.VectorError as verr
import arq.exceptions.MemoryError as merr
import komm


class Decoder:
    def __init__(self):
        self.__received_segment = numpy.array([])
        self.__decoded_segment = numpy.array([])

    def decode_segment(self) -> bool:
        """
        Dekoduje otrzymany segment i zapisuje odkodowany ciąg w pamięci dekodera.

        :raises MemoryError: przy próbie dekodowania, gdy w pamięci dekodera nie ma segmentu
        :return: True, gdy segment jest poprawny. False, gdy jest niepoprawny.
        """
        pass

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


# Dekoder bitu parzystości
class ParityBitDecoder(Decoder):
    def __init__(self, segment_length: int):
        """
        Tworzy dekoder bitu parzystości.

        :param segment_length: długość segmentu wychodzącego z kodera (dane + PB)
        """
        super().__init__()
        self.__decoding_machine = komm.SingleParityCheckCode(segment_length)

    def decode_segment(self) -> bool:
        if len(self._Decoder__received_segment) == 0:
            raise merr.MemoryError("brak segmentu do zdekodowania", merr.MemoryErrorCodes.ELEMENT_NOT_EXIST)

        syndrom = self._Decoder__received_segment @ self.__decoding_machine.parity_check_matrix.T
        syndrom %= 2
        if syndrom.sum() % 2 != 0:
            return False

        self._Decoder__decoded_segment = self.__decoding_machine.decode(self._Decoder__received_segment)
        return True


# Dekoder - BCH
class BCHDecoder(Decoder):
    def __init__(self, control_positions: int, correcting_capability: int):
        """
        Tworzy dekoder kodu BCH.

        :param control_positions: ilość pozycji kontrolnych (mu)
        :param correcting_capability: ilość możliwych do naprawienia błędów
        """
        super().__init__()
        self.__decoding_machine = komm.BCHCode(control_positions, correcting_capability)

    def decode_segment(self) -> bool:
        if len(self._Decoder__received_segment) == 0:
            raise merr.MemoryError("brak segmentu do zdekodowania", merr.MemoryErrorCodes.ELEMENT_NOT_EXIST)

        syndrom = self._Decoder__received_segment @ self.__decoding_machine.parity_check_matrix.T
        syndrom %= 2
        if syndrom.sum() != 0:
            return False

        self._Decoder__decoded_segment = self.__decoding_machine.decode(self._Decoder__received_segment)
        return True


# Dekoder - powielenie bitu
class RepetitionCodeDecoder(Decoder):
    def __init__(self, repetition: int):
        """
        Tworzy dekoder kodu powielenia bitu.

        :param repetition: ilość powtórzeń bitu
        """
        super().__init__()
        self.__decoding_machine = komm.RepetitionCode(repetition)

    def decode_segment(self) -> bool:
        if len(self._Decoder__received_segment) == 0:
            raise merr.MemoryError("brak segmentu do zdekodowania", merr.MemoryErrorCodes.ELEMENT_NOT_EXIST)

        syndrom = self._Decoder__received_segment @ self.__decoding_machine.parity_check_matrix.T
        syndrom %= 2
        if syndrom.sum() != 0:
            return False

        self._Decoder__decoded_segment = self.__decoding_machine.decode(self._Decoder__received_segment)
        return True


# Dekoder - kod Hamminga
class HammingDecoder(Decoder):
    def __init__(self, control_positions: int):
        """
        Tworzy dekoder kodu Hamminga.

        :param control_positions: ilość pozycji kontrolnych
        """
        super().__init__()
        self.__decoding_machine = komm.HammingCode(control_positions)

    def decode_segment(self) -> bool:
        if len(self._Decoder__received_segment) == 0:
            raise merr.MemoryError("brak segmentu do zdekodowania", merr.MemoryErrorCodes.ELEMENT_NOT_EXIST)

        syndrom = self._Decoder__received_segment @ self.__decoding_machine.parity_check_matrix.T
        syndrom %= 2
        if syndrom.sum() != 0:
            return False

        self._Decoder__decoded_segment = self.__decoding_machine.decode(self._Decoder__received_segment)
        return True


# Dekoder - kod cykliczny
class CyclicDecoder(Decoder):
    def __init__(self, polynomial: int, segment_length: int):
        """
        Tworzy dekoder kodu cyklicznego.

        :param polynomial: wielomian generujący
        :param segment_length: długość słowa kodowego
        """
        super().__init__()
        self.__decoding_machine = komm.CyclicCode(segment_length, generator_polynomial=polynomial)

    def decode_segment(self) -> bool:
        if len(self._Decoder__received_segment) == 0:
            raise merr.MemoryError("brak segmentu do zdekodowania", merr.MemoryErrorCodes.ELEMENT_NOT_EXIST)

        syndrom = self._Decoder__received_segment @ self.__decoding_machine.parity_check_matrix.T
        syndrom %= 2
        if syndrom.sum() != 0:
            return False

        self._Decoder__decoded_segment = self.__decoding_machine.decode(self._Decoder__received_segment)
        return True