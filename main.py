from arq import Source as SourceModule
from arq import Encoder as EncoderModule
from arq import Channel as ChannelModule
from arq import Decoder as DecoderModule
from arq import SenderController as SenderCtrlModule
from arq import ReceiverController as ReceiverCtrlModule
from arq import Receiver as ReceiverModule
import numpy as n

codeword_length = 8
error_probability = 0.01

# Entry point narzędzia symulacyjnego
def main():
    # Źródło generuje wiadomość w formie ciągu bitów
    source = SourceModule.Source()
    original_message = source.pop_message()
    print("Wiadomość przed wysłaniem:\t\t", original_message)

    # Koder pobiera wiadomość
    encoder = EncoderModule.Encoder()
    encoder.push_message(original_message, codeword_length)

    # Koder wysyła segmenty do kontrolera transmisji nadawcy
    # Ten wysyła segment przez kanał, czeka na odpowiedź
    # Jeżeli przyjdzie potwierdzenie odbioru, to wysyłamy kolejny segment
    # Jeżeli przyjdzie żądanie retransmisji, to wysyłamy ponownie tą samą wiadomość
    channel = ChannelModule.Channel(error_probability)
    sender_controller = SenderCtrlModule.SenderController()
    receiver_controller = ReceiverCtrlModule.ReceiverController()
    decoder = DecoderModule.Decoder(codeword_length)

    print("")
    while True:
        segment_from_encoder = encoder.pop_segment()
        if len(segment_from_encoder) == 0:
            break

        print("Wysłano segment z kodera:\t\t", segment_from_encoder)
        sender_controller.push_segment(segment_from_encoder)
        while True:
            channel.send_segment(sender_controller.pop_segment())

            # Dekoder odbiera segment i odkodowuje go
            # Jeżeli segment jest niepoprawny, to nie dokonujemy retransmisji
            segment_from_channel = channel.receive_segment()
            decoder.push_segment(segment_from_channel)
            response = decoder.decode_segment()
            if response:
                break
            else:
                print("Odebrano błędny segment:\t\t", segment_from_channel)
                decoder.pop_segment()

        # Jeżeli dekoder odebrał dobry semgnet, to wysyła go do kontrolera transmisji
        segment_from_decoder = decoder.pop_segment()
        print("Odebrano segment z dekodera:\t", segment_from_decoder)
        receiver_controller.push_message(segment_from_decoder)

    # Do przesłaniu całej wiadomości kontroler odbiorcy zwraca scaloną wiadomość
    received_message = receiver_controller.pop_message()
    print("\nOtrzymana wiadomość:\t\t\t", received_message)

    receiver = ReceiverModule.Receiver()
    receiver.receive_message(received_message, original_message)
    receiver.save_statistics("stats")


if __name__ == "__main__":
    main()
