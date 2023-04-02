import unittest

import arq.Channel as ChannelModule
import numpy
import arq.exceptions.VectorError as verr
import arq.exceptions.MemoryError as cherr


class MyTestCase(unittest.TestCase):

    # Wysłanie do kanału niepustego semgnetu, gdy kanał jesy pusty
    def testChannel_send_non_empty_segment(self):
        channel = ChannelModule.Channel(0.5)
        segment = numpy.array([0, 0, 0, 1])
        channel.send_segment(segment)

        for i in range(len(channel.segment())):
            self.assertEqual(channel.segment()[i], segment[i])

    # Wysłanie do kanału pustego segmentu
    def testChannel_send_empty_segment(self):
        channel = ChannelModule.Channel(0.5)
        segment = numpy.array([])

        with self.assertRaises(verr.VectorError):
            channel.send_segment(segment)

    # Wysłanie do kanału segmentu, który zawiera błędne dane
    def testChannel_send_invalid_segment(self):
        channel = ChannelModule.Channel(0.5)
        segment = numpy.array([0, 0, 1, 3, 0, 1])

        with self.assertRaises(verr.VectorError):
            channel.send_segment(segment)

    # Wysłanie do kanału segmentu, gdy kanał jest pełny
    def testChannel_send_channel_busy(self):
        channel = ChannelModule.Channel(0.5)
        segment = numpy.array([0, 0, 1])
        channel.send_segment(segment)

        with self.assertRaises(cherr.MemoryError):
            channel.send_segment(segment)

    # Odebranie segmentu z kanału
    def testChannel_receive_channel_not_empty(self):
        channel = ChannelModule.Channel(1)
        segment = numpy.array([1, 0, 1, 0, 1, 0, 1, 1])
        channel.send_segment(segment)
        received_segment = channel.receive_segment()

        self.assertEqual(len(received_segment), len(segment))
        self.assertEqual(len(channel.segment()), 0)

        for i in range(len(channel.segment())):
            self.assertNotEqual(channel.segment()[i], segment[i])

    # Odebranie segmentu z pustego kanału
    def testChannel_receive_channel_empty(self):
        channel = ChannelModule.Channel(1)
        received_segment = channel.receive_segment()

        self.assertEqual(len(received_segment), 0)
        self.assertEqual(len(channel.segment()), 0)

if __name__ == '__main__':
    unittest.main()
