import websocket
from queue import Queue
import threading
import json, time
from pydantic import BaseModel


class Packet(BaseModel):
    sender: str
    paddle_y: int
    ball_position: tuple[int, int]
    ball_velocity: tuple[int, int]
    score: list[int]


HOST_ADDRESS = "ws://viktor.asker.shop:443/ws"
ROOM_ID = "PONG"
PLAYER_NAME = "Viktor"
ROLE = "HOST"


def send_packet(input_queue: Queue, packet: Packet):
    input_queue.put_nowait(json.dumps(packet.model_dump()))


def receive_packet(output_queue: Queue) -> Packet:
    return Packet(**json.loads(output_queue.get()))


class NetworkedClient:
    def __init__(self) -> None:
        self.latest_recived_packet = None

    def run(self, input_queue: Queue, output_queue: Queue):
        self.websocket = websocket.WebSocketApp(
            HOST_ADDRESS,
            on_message=lambda ws, message: self.on_message(ws, message, output_queue),
            on_close=lambda ws, close_status_code, close_msg: self.on_close(
                ws, close_status_code, close_msg
            ),
            on_error=lambda ws, error: self.on_error(ws, error),
            on_open=lambda ws: self.on_open(ws, input_queue),
        )

        self.websocket.run_forever(reconnect=5)

    def send_packets(self, ws: websocket.WebSocketApp, input_queue: Queue):
        try:
            while True:
                packet = input_queue.get()
                ws.send(packet)
        except Exception as e:
            print(f"Error sending packet: {e}")

    def on_open(self, ws: websocket.WebSocketApp, input_queue: Queue):
        print("Opened connection")
        ws.send_text(ROOM_ID)
        threading.Thread(target=self.send_packets, args=(ws, input_queue)).start()

    def on_message(self, ws, message, output_queue: Queue):
        try:
            packet_json = json.loads(message)
            packet = Packet(**packet_json)
            print(f"received packet: {message}")
            output_queue.put_nowait(message)
        except json.JSONDecodeError:
            print("Invalid packet received")

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("### closed ###")


def connect() -> None:
    client = NetworkedClient()
    input_queue = Queue()
    output_queue = Queue()
    threading.Thread(target=client.run, args=(input_queue, output_queue)).start()
    return input_queue, output_queue
