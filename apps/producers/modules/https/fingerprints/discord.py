import zlib
import pyzstd
import erlpack
import json
import urllib.parse

def decode_querystring(querystring: str) -> dict[str, str]:
    data = urllib.parse.parse_qs(querystring, keep_blank_values=True)
    result = {}
    for key, value in data.items():
        if len(value) != 1:
            print(f"query parameter '{key}' has been specified multiple times")
            continue
        result[key] = value[0]
    return result

def deserialize_erlpackage(payload):
    if isinstance(payload, bytes):
        return payload.decode()
    elif isinstance(payload, erlpack.Atom):
        return str(payload)
    elif isinstance(payload, list):
        return [deserialize_erlpackage(i) for i in payload]
    elif isinstance(payload, dict):
        deserialized = {}
        for k, v in payload.items():
            deserialized[deserialize_erlpackage(k)] = deserialize_erlpackage(v)
        return deserialized
    else:
        return payload

class DiscordMessageGatewayIntercept:
    decoder = None
    decoderType = None

    def __init__(self, websocket_connection_info):
        # Parse the compression from path
        compression = websocket_connection_info["path"].split("compress=")[1]
        websocket_connection_info["compression"] = compression.split("&")[0]

        self.decoder = None
        if websocket_connection_info["compression"] == "zlib-stream":
            self.decoder = zlib.decompressobj()
            self.decoderType = "zlib"
        elif websocket_connection_info["compression"] == "zstd-stream":
            self.decoder = pyzstd.ZstdDecompressor()
            self.decoderType = "zstd"

    def handle_message(self, data: bytes):
        if self.decoder is not None:
            if self.decoderType == "zlib" and not data.endswith(b'\x00\x00\xff\xff'):
                print("Received incomplete zlib stream")
                return None

            try:
                decoded = self.decoder.decompress(data)
                print(decoded)
                return decoded
            except Exception as e:
                print(f"Error decompressing data: {e}")
        else:
            print("No decoder set for DiscordMessageGatewayIntercept - Invalid compression scheme?")

def getModule():
    return {
        "name": "Discord",
        "hostname": "gateway.discord.gg",
        "method": "WS",
        "processingClass": DiscordMessageGatewayIntercept
    }