# Koder - wersja deweloperska
# - Segmentuje wiadomość
# - Dokłada do segmentów narzut związany z kodowaniem
# - Przekazuje segmenty do kontrolera transmisji nadawcy


import numpy

SEGMENT_LENGTH = 8
class Encoder:
    # -----------------------------------------------------------------------
    # Wprowadza wiadomość bitową do kodera.
    #
    # Parametry:
    # message - wiadomość bitowa wchodząca do kodera
    #
    # Zwraca:
    # Nic.
    # -----------------------------------------------------------------------



# __init__
# length -> ile bitów w segmencie 
    def push_message(self, message: numpy.array, length=7):

        self.message = message
        self.counter = 0
        self.how_many_segments = (len(self.message) // length)+1
        self.segments = numpy.array_split(message, self.how_many_segments)

        for i in range(len(self.segments)):

            parity_bit = self.calcParityBit(self.segments[i])
            self.segments[i] = numpy.append(self.segments[i], parity_bit)

    # -----------------------------------------------------------------------
    # Wyciąga kolejny segment bitowy znajdujący się w pamięci kodera.
    #
    # Zwraca:
    # Kolejny segment segment bitowy z pamięci kodera.
    # -----------------------------------------------------------------------
    def pop_segment(self) -> numpy.array:

        if len(self.segments) != 0:
            segment: numpy.array = self.segments[0]
            self.segments.pop(0)
            return segment
        else:
            return numpy.array([])
        pass

    # def onAckknowledgment(self):
    #     if self.counter < len(self.segments):
    #         self.counter+=1
    #     else:
    #         pass
            # clear() 
            # jeśli wszystkie segmenty będą potwierdzone to clear pamięci encodera?

    # 0 jeśli parzysta, 1 jeśli nieparzysta
    def calcParityBit(self, segment: numpy.array) -> int:
        if numpy.count_nonzero(segment == 1) % 2 == 0:
            return 0
        else:
            return 1
