import unittest

import komm

import arq.Decoder as DecoderModule
import numpy
import arq.exceptions.VectorError as verr
import arq.exceptions.MemoryError as merr
import arq.Source as src
import arq.Channel as ch

class MyTestCase(unittest.TestCase):
    # Wczytanie do dekodera segmentu
    def testDecoder_receive_non_empty(self):
        channel_segment = numpy.array([1, 0, 1, 0])
        decoder = DecoderModule.ParityBitDecoder(len(channel_segment))
        decoder.push_segment(channel_segment)

        for i in range(len(decoder.segment())):
            self.assertEqual(decoder.segment()[i], channel_segment[i])

    # Wczytanie do dekodera pustego segmentu
    def testDecoder_receive_empty(self):
        channel_segment = numpy.array([])
        decoder = DecoderModule.ParityBitDecoder(4)

        with self.assertRaises(verr.VectorError):
            decoder.push_segment(channel_segment)

    # Wczytanie do dekodera niepoprawnego segmentu
    def testDecoder_receive_invalid(self):
        channel_segment = numpy.array([1, 0, 3, 1])
        decoder = DecoderModule.ParityBitDecoder(len(channel_segment))

        with self.assertRaises(verr.VectorError):
            decoder.push_segment(channel_segment)

    # Wczytanie do dekodera segmentu w momencie, gdy dekoder przetwarza inny kanał
    def testDecoder_receive_decoder_busy(self):
        channel_segment = numpy.array([1, 0, 1, 1])
        decoder = DecoderModule.ParityBitDecoder(len(channel_segment))
        decoder.push_segment(channel_segment)

        with self.assertRaises(merr.MemoryError):
            decoder.push_segment(channel_segment)

    # Dekoder nie ma segmentu, ale wywołano dekodowanie
    def testDecoder_decode_non_existing_segment(self):
        decoder = DecoderModule.ParityBitDecoder(10)

        with self.assertRaises(merr.MemoryError):
            decoder.decode_segment()

    # Odebranie segmentu z dekodera
    def testDecoder_pop_decoded_segment_from_decoder(self):
        decoder = DecoderModule.ParityBitDecoder(10)
        channel_segment = numpy.array([1, 0, 1, 0])
        decoder.push_segment(channel_segment)
        decoded_segment = decoder.pop_segment()

        for i in range(len(decoded_segment)):
            self.assertEqual(decoded_segment[i], channel_segment[i])
        self.assertEqual(len(decoder.segment()), 0)

    # Powielenie bitu - poprawny
    def testDecoder_repetition_code_valid(self):
        decoder = DecoderModule.RepetitionCodeDecoder(3)
        channel_segment = numpy.array([0, 0, 0])

        decoder.push_segment(channel_segment)
        self.assertTrue(decoder.decode_segment())
        decoded_segment = decoder.pop_segment()

        self.assertEqual(decoded_segment, [0])

    # Powielenie bitu - niepoprawny
    def testDecoder_repetition_code_invalid(self):
        decoder = DecoderModule.RepetitionCodeDecoder(3)
        channel_segment = numpy.array([0, 1, 0])

        decoder.push_segment(channel_segment)
        self.assertTrue(not decoder.decode_segment())

    # BCH - poprawny
    def testDecoder_BCH_code_valid(self):
        source = src.Source()
        message = source.pop_message(21)

        coder = komm.BCHCode(5, 2)
        encoded_msg = coder.encode(message)

        decoder = DecoderModule.BCHDecoder(5, 2)
        decoder.push_segment(encoded_msg)
        self.assertTrue(decoder.decode_segment())

        decoded_msg = decoder.pop_segment()
        self.assertEqual(len(message), len(decoded_msg))
        for i in range(0, len(message)):
            self.assertEqual(message[i], decoded_msg[i])

    # BCH - niepoprawny
    def testDecoder_BCH_code_invalid(self):
        source = src.Source()
        message = source.pop_message(21)

        coder = komm.BCHCode(5, 2)
        encoded_msg = coder.encode(message)

        encoded_msg[0] = not encoded_msg[0]

        decoder = DecoderModule.BCHDecoder(5, 2)
        decoder.push_segment(encoded_msg)
        self.assertTrue(not decoder.decode_segment())

    # Hamming - poprawny
    def testDecoder_Hamming_code_valid(self):
        source = src.Source()
        message = source.pop_message(57)

        coder = komm.HammingCode(6)
        encoded_msg = coder.encode(message)

        decoder = DecoderModule.HammingDecoder(6)
        decoder.push_segment(encoded_msg)
        self.assertTrue(decoder.decode_segment())

        decoded_msg = decoder.pop_segment()
        self.assertEqual(len(message), len(decoded_msg))
        for i in range(0, len(message)):
            self.assertEqual(message[i], decoded_msg[i])

    # Hamming - niepoprawny
    def testDecoder_Hamming_code_invalid(self):
        source = src.Source()
        message = source.pop_message(57)

        coder = komm.HammingCode(6)
        encoded_msg = coder.encode(message)

        encoded_msg[0] = not encoded_msg[0]

        decoder = DecoderModule.HammingDecoder(6)
        decoder.push_segment(encoded_msg)
        self.assertTrue(not decoder.decode_segment())

    # Cykliczny - poprawny
    def testDecoder_Cyclic_code_valid(self):
        source = src.Source()
        message = source.pop_message(4)

        coder = komm.CyclicCode(7, generator_polynomial=0b1011)
        encoded_msg = coder.encode(message)

        decoder = DecoderModule.CyclicDecoder(0b1011, 7)
        decoder.push_segment(encoded_msg)
        self.assertTrue(decoder.decode_segment())

        decoded_msg = decoder.pop_segment()
        self.assertEqual(len(message), len(decoded_msg))
        for i in range(0, len(message)):
            self.assertEqual(message[i], decoded_msg[i])

    # Cykliczny - niepoprawny
    def testDecoder_Cyclic_code_invalid(self):
        source = src.Source()
        message = source.pop_message(4)

        coder = komm.CyclicCode(7, generator_polynomial=0b1011)
        encoded_msg = coder.encode(message)

        encoded_msg[0] = not encoded_msg[0]

        decoder = DecoderModule.CyclicDecoder(0b1011, 7)
        decoder.push_segment(encoded_msg)
        self.assertTrue(not decoder.decode_segment())



if __name__ == '__main__':
    unittest.main()
