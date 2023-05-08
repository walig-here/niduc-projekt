from arq import Source as SourceModule
from arq import Encoder as EncoderModule
from arq import Channel as ChannelModule
from arq import Decoder as DecoderModule
from arq import SenderController as SenderCtrlModule
from arq import ReceiverController as ReceiverCtrlModule
from arq import Receiver as ReceiverModule
from arq import Configuration as Config
import numpy

class ARQ:

    def __init__(self, message_length: int, turns: int, file_name: str):
        #Config.configure_simulation()
        #Config.configure_encoding(self.encoder, self.decoder)
        #Config.configure_channel(self.channel)

        self.source = SourceModule.Source()
        self.sender_controller = SenderCtrlModule.SenderController()
        self.receiver_controller = ReceiverCtrlModule.ReceiverController()
        self.receiver = ReceiverModule.Receiver()

        # temp
        self.channel = ChannelModule.Channel(10E-9, 0.1, 0.75)
        self.encoder = EncoderModule.PBEncoder()
        self.decoder = DecoderModule.ParityBitDecoder(33)

    def simulate_transmission(self, message_length, segment_length):
        # Źródło generuje wiadomość w formie ciągu bitów
        original_message = self.source.pop_message(message_length)
        error_count = numpy.uint(0)

        # Koder pobiera wiadomość
        self.encoder.push_message(original_message, segment_length)

        # Koder wysyła segmenty do kontrolera transmisji nadawcy
        # Ten wysyła segment przez kanał, czeka na odpowiedź
        # Jeżeli przyjdzie potwierdzenie odbioru, to wysyłamy kolejny segment
        # Jeżeli przyjdzie żądanie retransmisji, to wysyłamy ponownie tą samą wiadomość

        self.channel.reset_bit_counter()
        while True:
            segment_from_encoder = self.encoder.pop_segment()
            if len(segment_from_encoder) == 0:
                break

            while True:
                self.channel.send_segment(segment_from_encoder)

                # Dekoder odbiera segment i odkodowuje go
                # Jeżeli segment jest niepoprawny, to nie dokonujemy retransmisji
                segment_from_channel = self.channel.receive_segment()
                self.decoder.push_segment(segment_from_channel)
                response = self.decoder.decode_segment()
                if response:
                    break
                else:
                    self.decoder.pop_segment()
                    error_count += 1

            # Jeżeli dekoder odebrał dobry semgnet, to wysyła go do kontrolera transmisji
            segment_from_decoder = self.decoder.pop_segment()
            self.receiver_controller.push_segment(segment_from_decoder)

        # Do przesłaniu całej wiadomości kontroler odbiorcy zwraca scaloną wiadomość
        received_message = self.receiver_controller.pop_message()

        self.receiver.set_error_count(error_count)
        self.receiver.receive_message(received_message, original_message, error_count)

    def save_results(self, file_name):
        self.receiver.save_statistics(file_name+".csv")