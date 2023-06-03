# Kanał transmisyjny - wersja deweloperska
# - Odbiera segmenty
# - Przekłamuje bity z pewnym prawdopodobieństwem
# ========================================================================
# Kanał - wersja ultimate
# - przejście na model Gilberta
# - mechanizm zliczający przesłane przez kanał bity
import enum
import random

import numpy
import komm
import arq.exceptions.VectorError as verr
import arq.exceptions.MemoryError as cherr


class ChannelStates(enum.Enum):
    BSC = 0     # przekłamywanie bitów
    SERIES = 1  # przekłamywanie bitów seriami

class Channel:
    def __init__(self, error_rate: float, series_probability: float, bsc_probability: float):
        """
        Konstruktior dla kanału transmisyjnego.

        :param error_rate: stopa błędów kanału w trybie BSC
        :param series_probability: prawdopodobieństwo przejścia z BSC do SERIES
        :param bsc_probability: prawdopodobieństwo przejścia z SERIES do BSC
        """
        if error_rate > 1:
            error_rate = 1

        self.__channel_segment = numpy.array([])        # segment przesyłany przez kanał
        self.__error_rate = error_rate                  # stopa błędu kanału w trybie BSC
        self.__bit_counter = 0                          # licznik bitów przechodzących przez kanał
        self.__channel_mode = ChannelStates.BSC         # aktualny tryb działanai kanału
        self.__series_probability = series_probability  # prawd. przejścia z BSC do SERIES
        self.__bsc_probability = bsc_probability        # prawd. przejścia z SERIES do BSC

    def reset_bit_counter(self):
        """
        Resteuje mechanizm liczający bity, które przepłynęły przez kanał.
        """
        self.__bit_counter = 0

    def get_bit_count(self) -> int:
        """
        Zwraca ilość bitów, które przepłyneły przez kanał od czasu ostatniej transmisji.
        """

        return self.__bit_counter

    def segment(self) -> numpy.array:
        """
        WŁĄCZNIE NA POTRZEBY TESTÓW JEDNOSTKOWYCH!

        Pobiera segment z kanału, z pominięciem przekłamań wynikających z
        transmisji.

        :return: Segment przepływający przez kanał.
        """

        return self.__channel_segment

    def send_segment(self, segment: numpy.array):
        """
        Wprowadza segment bitowy do kanału. Dodatkowo przeprowadza kontrolę poprawności
        wprowadzanego segmentu. Nie dopuszcza do wprowadzenia nowego segmentu, gdy w kanale
        znajduje się juz jakiś segment.

        :param segment: segment bitowy wchodzący do kanału
        :raises VectorError: gdy podano wektor niebitowy lub pusty.
        :raises ChannelError: gdy w kanale znajduje się już jakiś segment, a nastąpiła próba wprowadzenia kolejnego.
        """

        if len(self.__channel_segment) != 0:
            raise cherr.MemoryError("kanał zajęty", cherr.MemoryErrorCodes.OCCUPIED)
        if len(segment) == 0:
            raise verr.VectorError("wektor jest pusty", verr.VectorErrorCodes.EMPTY)
        if not numpy.all(numpy.logical_or(segment == 0, segment == 1)):
            raise verr.VectorError("wektor nie jest binarny", verr.VectorErrorCodes.NON_BINARY)

        self.__channel_segment = segment
        self.__bit_counter += len(segment)

    def __burden(self):
        """
        Obciąża aktualnie zawarty w kanale segment błędami transmisji. Rodzaj generowanych błędów zależy od trybu, w
        w jakim działa kanał. Działa on w modelu generowania błędów Gilberta.
        """

        # gdy w kanale nie ma segmentu to nie ma czego obciążać błędami
        if len(self.__channel_segment) == 0:
            return

        # przejście między trybami
        self.__transmission()

        # dobór sposobu generowania błędów w zależności od trybu kanału
        if self.__channel_mode == ChannelStates.BSC:
            error_generator = komm.BinarySymmetricChannel(self.__error_rate)
        else:
            error_generator = komm.BinarySymmetricChannel(self.__error_rate * 10E3)

        # generowanie błędu
        self.__channel_segment = error_generator(self.__channel_segment)

    def __transmission(self):
        """
        Odpowiada za wykonanie przejścia między stanami kanału.
        """
        rng = random.Random()

        # przejście BSC -> SERIES
        if self.__channel_mode == ChannelStates.BSC and rng.random() < self.__series_probability:
            self.__channel_mode = ChannelStates.SERIES
        # przejście SERIES -> BSC
        elif self.__channel_mode == ChannelStates.SERIES and rng.random() < self.__bsc_probability:
            self.__channel_mode = ChannelStates.BSC

    def receive_segment(self) -> numpy.array:
        """
        Wyprowadza segment bitowy z kanału. Zwalnia tym samym kanał dla nowego segmentu.
        Wyprowadzony segment jest obciążany błędami transmisji, występującymi w kanale.

        :return: Zawarty w kanale segment, obciążony błędami transmisji.
        """

        self.__burden()
        channel = self.__channel_segment
        self.__channel_segment = numpy.array([])
        return channel
