import websocket
import threading
import time
import json
from pydantic import BaseModel


class Packet(BaseModel):
    sender: str
    paddle_y: int
    ball_position: tuple[int, int]
    ball_velocity: tuple[int, int]
    score: tuple[int, int]


HOST_ADDRESS = "ws://viktor.asker.shop:443/ws"
ROOM_ID = "PONG"
PLAYER_NAME = "Viktor"


class NetworkedClient:
    def __init__(self) -> None:
        self.latest_recived_packet = None

    def run(self):
        self.websocket = websocket.WebSocketApp(
            HOST_ADDRESS,
            on_message=lambda ws, message: self.on_message(ws, message),
            on_close=lambda ws, close_status_code, close_msg: self.on_close(
                ws, close_status_code, close_msg
            ),
            on_error=lambda ws, error: self.on_error(ws, error),
            on_open=lambda ws: self.on_open(ws),
        )

        self.websocket.run_forever(reconnect=5)

    def send_packet(self, packet: Packet):
        self.websocket.send(json.dumps(packet.model_dump()))

    def on_open(self, ws: websocket.WebSocketApp):
        print("Opened connection")
        ws.send_text(ROOM_ID)
        # threading.Thread(target=ping_chat_room, args=(ws,), daemon=True).start()

    def on_message(self, ws, message):
        try:
            # packet_json = json.loads(message)
            # packet = Packet(**packet_json)
            self.latest_recived_packet = message
        except json.JSONDecodeError:
            print("Invalid packet received")

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("### closed ###")


def main() -> None:
    client = NetworkedClient()
    threading.Thread(target=client.run, daemon=True).start()


if __name__ == "__main__":
    main()
