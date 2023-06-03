from arq import Encoder as EncoderModule
from arq import Channel as ChannelModule
from arq import Decoder as DecoderModule


# Wczytuje konfigurację aplikacji - z simulation.config
# - ilość prób
# - nazwa pliku wyjściowego
# - długość wiadomości
def configure_simulation():
    config = {}
    with open("simulation.config") as f:
        for line in f:
            line = line.strip()  # usunięcie białych znaków z końca i początku linii
            if not line:  # pomijanie pustych linii
                continue
            key, value = line.split("=")
            config[key] = value

    if len(config) == 0:
        return 0, 'result', 0

    number_of_trials = int(config['number_of_trials'])
    output_file_name = config['output_file_name']
    message_length = int(config['message_length'])

    return number_of_trials, output_file_name, message_length


# Wczytuje konfigurację kanału - channel.config
# - BER
# - parametry kanału
def configure_channel():
    config = {}
    with open("channel.config") as f:
        for line in f:
            line = line.strip()  # usunięcie białych znaków z końca i początku linii
            if not line:  # pomijanie pustych linii
                continue
            key, value = line.split("=")
            config[key] = value

    if len(config) == 0:
        return 0, 'result', 0

    error_rate = float(config['error_rate'])
    series_probability = float(config['series_probability'])
    bsc_probability = float(config['bsc_probability'])

    channel = ChannelModule.Channel(error_rate, series_probability, bsc_probability)

    return channel


# Wczytuje konfiguację kodera/dekodera - encoding.config
# - ilość segmentów
# - typ kodowania
def configure_encoding():
    config = {}
    with open("encoding.config") as f:
        for line in f:
            line = line.strip()  # usunięcie białych znaków z końca i początku linii
            if not line:  # pomijanie pustych linii
                continue
            key, value = line.split("=")
            config[key] = value

    if len(config) == 0:
        return 0, 'result', 0

    encoding_type = config['encoding_type']

    # Bit parzystości - parametry:
    # number_of_segments
    if encoding_type == "PB":
        segment_length = int(config['segment_length'])                  # gługość sgementu, do którego dołączny jest PB
        encoder = EncoderModule.PBEncoder(segment_length)
        decoder = DecoderModule.ParityBitDecoder(segment_length)

    # BCH - parametry:
    # control_positions
    # correcting_capability
    elif encoding_type == "BCH":
        control_positions = int(config['control_positions'])            # mu
        correcting_capability = int(config['correcting_capability'])    # tau
        encoder = EncoderModule.BCHEncoder(control_positions, correcting_capability)
        decoder = DecoderModule.BCHDecoder(control_positions, correcting_capability)

    # Hamming - parametry:
    # control_positions
    # correcting_capability
    elif encoding_type == "HM":
        control_positions = int(config['control_positions'])        # mu
        encoder = EncoderModule.HammingEncoder(control_positions)
        decoder = DecoderModule.HammingDecoder(control_positions)

    # Nieznany kod
    else:
        encoder = EncoderModule.Encoder()
        decoder = DecoderModule.Decoder()

    return encoder, decoder
