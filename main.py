import numpy

import arq.Channel as ch


# Entry point narzędzia symulacyjnego
def main():
    channel = ch.Channel(0.1)
    segment = numpy.array([1, 0, 1])
    channel.send_segment(segment)
    segment = channel.receive_segment()
    print(segment)
    

if __name__ == "__main__":
    main()
