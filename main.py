from arq.Encoder import Encoder
from arq.Source import Source
from arq.SenderController import SenderController
import numpy
# Entry point narzędzia symulacyjnego
def main():
    
    src = Source()
    message = src.pop_message()
    print(f'Message {message}')
    enc = Encoder()
    enc.push_message(message)
    print(f'ile segmentow {(enc.how_many_segments)}')
    
    sendContr = SenderController()
    
    sendContr.push_segment(enc.pop_segment)
    while numpy.size(sendContr.segment) != 0:
        segment = sendContr.pop_segment()
        print(f'Segment {segment}')
        ack = numpy.random.choice([True, False])

        sendContr.push_response(ack)
        if not ack:
            print("Żądanie retransmisji")
        else:
            sendContr.push_segment(enc.pop_segment())


if __name__ == "__main__":
    main()
