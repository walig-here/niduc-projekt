import unittest
import arq.Decoder as DecoderModule
import numpy
import arq.exceptions.VectorError as verr
import arq.exceptions.MemoryError as merr

class MyTestCase(unittest.TestCase):
    # Wczytanie do dekodera segmentu
    def testDecoder_receive_non_empty(self):
        channel_segment = numpy.array([1, 0, 1, 0])
        decoder = DecoderModule.Decoder(len(channel_segment))
        decoder.push_segment(channel_segment)

        for i in range(len(decoder.segment())):
            self.assertEqual(decoder.segment()[i], channel_segment[i])

    # Wczytanie do dekodera pustego segmentu
    def testDecoder_receive_empty(self):
        channel_segment = numpy.array([])
        decoder = DecoderModule.Decoder(4)

        with self.assertRaises(verr.VectorError):
            decoder.push_segment(channel_segment)

    # Wczytanie do dekodera niepoprawnego segmentu
    def testDecoder_receive_invalid(self):
        channel_segment = numpy.array([1, 0, 3, 1])
        decoder = DecoderModule.Decoder(len(channel_segment))

        with self.assertRaises(verr.VectorError):
            decoder.push_segment(channel_segment)

    # Wczytanie do dekodera segmentu w momencie, gdy dekoder przetwarza inny kanał
    def testDecoder_receive_decoder_busy(self):
        channel_segment = numpy.array([1, 0, 1, 1])
        decoder = DecoderModule.Decoder(len(channel_segment))
        decoder.push_segment(channel_segment)

        with self.assertRaises(merr.MemoryError):
            decoder.push_segment(channel_segment)

    # Dekoder wykrywa poprawny kod
    def testDecoder_decode_valid_segment(self):
        channel_segment = numpy.array([1, 1, 1, 1, 0])
        decoder = DecoderModule.Decoder(len(channel_segment))
        decoder.push_segment(channel_segment)

        self.assertEqual(decoder.decode_segment(), True)

    # Dekoder wykrywa niepoprawny kod
    def testDecoder_decode_invalid_segment(self):
        channel_segment = numpy.array([1, 0, 1, 1, 0])
        decoder = DecoderModule.Decoder(len(channel_segment))
        decoder.push_segment(channel_segment)

        self.assertEqual(decoder.decode_segment(), False)

    # Dekoder wykrywa niepoprawny (za krótki) kod
    def testDecoder_decode_to_short_segment(self):
        channel_segment = numpy.array([1, 1, 0])
        decoder = DecoderModule.Decoder(10)
        decoder.push_segment(channel_segment)

        self.assertEqual(decoder.decode_segment(), False)

    # Dekoder nie ma segmentu, ale wywołano dekodowanie
    def testDecoder_decode_non_existing_segment(self):
        decoder = DecoderModule.Decoder(10)

        with self.assertRaises(merr.MemoryError):
            decoder.decode_segment()

    # Odebranie segmentu z dekodera
    def testDecoder_pop_decoded_segment_from_decoder(self):
        decoder = DecoderModule.Decoder(10)
        channel_segment = numpy.array([1, 0, 1, 0])
        decoder.push_segment(channel_segment)
        decoded_segment = decoder.pop_segment()

        for i in range(len(decoded_segment)):
            self.assertEqual(decoded_segment[i], channel_segment[i])
        self.assertEqual(len(decoder.segment()), 0)


if __name__ == '__main__':
    unittest.main()
