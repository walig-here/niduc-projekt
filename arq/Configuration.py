from arq import Encoder as EncoderModule
from arq import Channel as ChannelModule
from arq import Decoder as DecoderModule


# Wczytuje konfigurację aplikacji
# - ilość prób
# - nazwa pliku wyjściowego
# - długość wiadomości
def configure_simulation():
    pass


# Wczytuje konfigurację kanału
# - ilość segmentów
# - typ kodowania
def configure_channel(channel: ChannelModule.Channel):
    pass


# Wczytuje konfiguację kodera/dekodera
# - BER
# - parametry kanału
def configure_encoding(encoder: EncoderModule.Encoder, decoder: DecoderModule.Decoder):
    pass
