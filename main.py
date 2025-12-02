import asyncio
from websocket_handler import websocket_connection

if __name__ == "__main__":
    asyncio.run(websocket_connection())