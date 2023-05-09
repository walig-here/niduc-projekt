# Koder - wersja deweloperska
# - Segmentuje wiadomość
# - Dokłada do segmentów narzut związany z kodowaniem
# - Przekazuje segmenty do kontrolera transmisji nadawcy


import numpy
SEGMENT_LENGTH = 8

class Encoder:
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
    def push_message(self, message: numpy.array, codeword_length: int):
        self.message = message
        self.counter = 0
        self.how_many_segments = (len(self.message) // codeword_length)
        self.segments = numpy.split(message, self.how_many_segments)
        self.encode_message()

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

class PBEncoder(Encoder):
    def encode_message(self):
        for i in range(len(self.segments)):
            parity_bit = self.calcParityBit(self.segments[i])
            self.segments[i] = numpy.append(self.segments[i], parity_bit)

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


# Koder - wersja deweloperska
# - Segmentuje wiadomość
# - Dokłada do segmentów narzut związany z kodowaniem
# - Przekazuje segmenty do kontrolera transmisji nadawcy
# ========================================================================
# Koder - wersja ultimate
# - kody cykliczne
# - kody BCH
# - kody Hamminga
# - kody z powieleniem bitu


import numpy

class Encoder:
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
    def push_message(self, message: numpy.array, codeword_length: int):
        self.codeworth_length = codeword_length
        self.message = message
        self.how_many_segments = (len(self.message) // codeword_length)
        self.segments = numpy.split(message, self.how_many_segments)
        self.encode_message()

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

class PBEncoder(Encoder):
    def encode_message(self):
        for i in range(len(self.segments)):
            parity_bit = self.calcParityBit(self.segments[i])
            self.segments[i] = numpy.append(self.segments[i], parity_bit)
    # 0 jeśli parzysta, 1 jeśli nieparzysta
    def calcParityBit(self, segment: numpy.array) -> int:
        if numpy.count_nonzero(segment == 1) % 2 == 0:
            return 0
        else:
            return 1


#działa ale trzeba podać odpowiednio długą wiadomośc do parametru mu i tau
#przykład
#code = BCHCode(6, 7)
#(code.length, code.dimension, code.minimum_distance)
#(63, 24, 15)
# długość wiadomość x *  24 gdzie x to ile segmentów będzie 

# import numpy as np
# from arq.Encoder import BCHEncoder
# enc = BCHEncoder(6, 7)
# mess = np.random.randint(2, size = 240)
# enc.push_message(mess)

# print(enc.pop_segment())

import komm

class BCHEncoder():
    def __init__(self, mu, tau):
        self.mu = mu
        self.tau = tau
        self.bch = komm.BCHCode(mu=self.mu, tau=self.tau)
    def push_message(self, message: numpy.array):
        
        # długość segmentu 
        self.segment_len = self.bch.dimension
        self.ilosc_segmentow = len(message) // self.segment_len
        self.segments = numpy.split(message, self.ilosc_segmentow)
        
        self.encode_message()
    def encode_message(self):

        for i in range(len(self.segments)):
            self.segments[i] = self.bch.encode(self.segments[i])
    
    
    def pop_segment(self) -> numpy.array:

        if len(self.segments) != 0:
            segment: numpy.array = self.segments[0]
            self.segments.pop(0)
            return segment
        else:
            return numpy.array([])

# ten równiez ma z góry narzucony dimension (wielkość segmentu)
# dla m = 5 dimension = 26

# np
# import numpy as np
# from arq.Encoders import HammingEncoder
# enc = HammingEncoder(5)
# mess = np.random.randint(2, size = 26*6)
# enc.push_message(mess)

# print(enc.pop_segment())

class HammingEncoder():
    def __init__(self, m, ext: bool = False):
        self.m = m
        
        self.hamming = komm.HammingCode(m=m, extended=ext)
    
    def push_message(self, message: numpy.array):
        
        # długość segmentu 
        segment_len = self.hamming.dimension
        self.ilosc_segmentow = len(message) // segment_len
        self.segments = numpy.split(message, self.ilosc_segmentow)
        self.encode_message()

    def encode_message(self):

        for i in range(len(self.segments)):
            self.segments[i] = self.hamming.encode(self.segments[i])
    
    
    def pop_segment(self) -> numpy.array:

        if len(self.segments) != 0:
            segment: numpy.array = self.segments[0]
            self.segments.pop(0)
            return segment
        else:
            return numpy.array([])
