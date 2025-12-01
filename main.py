#from websocket_handler import websocket_connection
#from sequence_runner import run_custom_sequence

#if __name__ == "__main__":
#   run_custom_sequence("item_4")

import asyncio
from websocket_handler import websocket_connection

if __name__ == "__main__":
   asyncio.run(websocket_connection())