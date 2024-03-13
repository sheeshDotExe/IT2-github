# import argparse
import os
from typing import Optional
import asyncio
import sys
import json
import yaml
import aiohttp
from typing import Any
from pathlib import Path
from loguru import logger

# import peerjs
from peerjs.peer import Peer, PeerOptions
from peerjs.peerroom import PeerRoom
from peerjs.util import util, default_ice_servers
from peerjs.enums import ConnectionEventType, PeerEventType
from aiortc.rtcconfiguration import RTCConfiguration, RTCIceServer

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PEER_ID_FILE_PATH = os.path.join(CURRENT_DIR, "peer_id.json")


def save_peer_id(peer_id: str):
    with open(PEER_ID_FILE_PATH, "w") as outfile:
        json.dump({"peerId": peer_id}, outfile)


def load_peer_id() -> Optional[str]:
    """Load and reuse saved peer ID if there is one."""
    conf_file = Path(PEER_ID_FILE_PATH)
    if conf_file.exists():
        conf = {}
        with conf_file.open() as infile:
            conf = yaml.load(infile, Loader=yaml.SafeLoader)
        if conf is not None:
            return conf.get("peerId", None)
        return None


async def join_peer_room(peer=None):
    """Join a peer room with other local peers."""
    # first try to find the remote peer ID in the same room
    room = PeerRoom(peer)
    logger.debug("Fetching room members...")
    peerIds = await room.getRoomMembers()
    logger.info("room members {}", peerIds)


class Client:
    def __init__(self) -> None:
        self.saved_peer_id: Optional[str] = load_peer_id()
        self.running = False
        self.shutdown = False
        self.create_peer()

    async def create_peer(self):
        logger.info("Creating peer")
        logger.info(f"Saved peer id: {self.saved_peer_id}")

        peer_token = util.randomToken()
        logger.info(f"Peer session token: {peer_token}")

        options = PeerOptions(
            token=peer_token,
            config=RTCConfiguration(
                iceServers=[RTCIceServer(**srv) for srv in default_ice_servers]
            ),
        )

        self.peer = Peer(id=self.saved_peer_id, peer_options=options)
        logger.info(f"Peer created with id: {self.peer.id}")

        await self.peer.start()
        logger.info(f"Peer started")

        self.running = True

        self.set_service_connection_handlers()

    async def make_discoverable(self):
        while not self.shutdown:
            logger.debug(f"Peer status: {self.peer}")
            try:
                if not self.peer or self.peer.destroyed:
                    logger.info("Peer destroyed. Will create a new peer.")
                    await self.create_peer()
                elif self.peer.open:
                    await join_peer_room(peer=self.peer)
                elif self.peer.disconnected:
                    logger.info("Peer disconnected. Will try to reconnect.")
                    await self.peer.reconnect()
                else:
                    logger.info(f"Peer still establishing connection. {self.peer}")
            except Exception as e:
                logger.exception(
                    "Error while trying to join local peer room. "
                    "Will retry in a few moments. "
                    "Error: \n{}",
                    e,
                )
                if self.peer and not self.peer.destroyed:
                    # something is not right with the connection to the server
                    # lets start a fresh peer connection
                    logger.info("Peer connection was corrupted. Detroying peer.")
                    await self.peer.destroy()
                    self.peer = None
                    logger.debug(f"peer status after destroy: {self.peer}")
            await asyncio.sleep(3)

    def handle_peer_connection(self, peer_connection):
        @peer_connection.on(ConnectionEventType.Open)
        async def peer_connection_open():
            logger.info("Connected to: {}", peer_connection.peer)

        @peer_connection.on(ConnectionEventType.Data)
        async def peer_connection_data(data: Any):
            logger.info(f"Data received from peer: {data}")

        @peer_connection.on(ConnectionEventType.Close)
        async def peer_connection_close():
            logger.info(f"Peer connection closed")

    def set_service_connection_handlers(self) -> None:
        # gets peer id from 0.peerjs.com:9000
        @self.peer.on(PeerEventType.Open)
        async def peer_open(id: str):
            logger.info(f"Peer signaling connection opened")
            if not self.peer.id:
                logger.info(f"Recived NULL id from peerjs server")
                self.peer.id = self.saved_peer_id
                return

            if self.saved_peer_id != self.peer.id:
                save_peer_id(self.peer.id)
                self.saved_peer_id = self.peer.id
                logger.info(f"Saved new peer id {self.peer.id} to file")

        @self.peer.on(PeerEventType.Disconnected)
        async def peer_disconnected(peer_id: str):
            logger.info(f"Peer {peer_id} disconnected from server.")
            # Workaround for peer.reconnect deleting previous id
            if not self.peer.id:
                logger.debug(
                    "BUG WORKAROUND: Peer lost ID. " "Resetting to last known ID."
                )
                self.peer._id = self.saved_peer_id
            self.peer._lastServerId = self.saved_peer_id

        @self.peer.on(PeerEventType.Close)
        def peer_close():
            logger.info("Peer connection closed")

        @self.peer.on(PeerEventType.Error)
        def peer_error(err):
            logger.exception("Peer error {err}")

        # remote peer tries to initiate connection
        @self.peer.on(PeerEventType.Connection)
        async def peer_connection(peer_connection):
            logger.info("Remote peer trying to establish connection")
            self.handle_peer_connection(peer_connection)


def create_client() -> None:
    client = Client()
    asyncio.get_event_loop().run_until_complete(client.make_discoverable())


def main() -> None:
    create_client()


if __name__ == "__main__":
    main()
