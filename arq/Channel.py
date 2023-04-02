# Kanał transmisyjny - wersja deweloperska
# - Odbiera segmenty
# - Przekłamuje bity z pewnym prawdopodobieństwem


import numpy
import komm
import arq.exceptions.VectorError as verr
import arq.exceptions.ChannelError as cherr


class Channel:
    def __init__(self, error_rate: float):
        self.__channel_segment = numpy.array([])
        self.__error_generator = komm.BinarySymmetricChannel(error_rate)

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
            raise cherr.ChannelError("kanał zajęty", cherr.ChannelErrorCodes.CHANNEL_IS_BUSY)
        if len(segment) == 0:
            raise verr.VectorError("wektor jest pusty", verr.VectorErrorCodes.EMPTY)
        if not numpy.all(numpy.logical_or(segment == 0, segment == 1)):
            raise verr.VectorError("wektor nie jest binarny", verr.VectorErrorCodes.NON_BINARY)

        self.__channel_segment = segment

    def __burden(self):
        """
        Obciąża aktualnie zawarty w kanale segment błędami transmisji.
        """

        if len(self.__channel_segment) == 0:
            return
        self.__channel_segment = self.__error_generator(self.__channel_segment)

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
