import json
import websockets
import asyncio
from concurrent.futures import ThreadPoolExecutor
from config import URL, SECRET_TOKEN
from sequence_runner import run_custom_sequence
from wrist_camera.websocket_video_stream import run_action_with_streaming

PRODUCT_TO_SEQUENCE = {
    "P001": "item_1",
    "P002": "item_2",
    "P003": "item_3",
    "P004": "item_4",
}

executor = ThreadPoolExecutor(max_workers=1)

async def websocket_connection(max_retries=3, retry_delay=5):
    attempt = 0
    while attempt < max_retries:
        try:
            print(f"Attempt {attempt + 1} of {max_retries} to connect...")
            async with websockets.connect(URL) as websocket:
                print("Connected to server")

                # Ping check
                try:
                    ping_waiter = await websocket.ping()
                    await ping_waiter
                    print("Ping successful")
                except Exception as e:
                    print(f"Ping failed: {e}")

                # Send INIT message
                init_msg = {
                    "sender_id": "UR_ARM_1",
                    "event": "INIT",
                    "payload": {
                        "token": SECRET_TOKEN,
                        "role": "ROBOT"
                    }
                }
                await websocket.send(json.dumps(init_msg))

                # Listen for messages
                async for message in websocket:
                    try:
                        message_data = json.loads(message)
                        event = message_data.get("event")
                        payload = message_data.get("payload", {})

                        print(f"EVENT: {event}")

                        if event == "CONNECTED":
                            print("Server is connected")
                        if event in ["PICK_AND_PLACE", "TEST_PICK_AND_PLACE"]:
                            product_code = payload.get("product", "P001")
                            sequence_name = PRODUCT_TO_SEQUENCE.get(product_code)

                        # pick and place product
                        if not sequence_name:
                            print(f"ERROR: No movement sequence mapped to product {product_code}")
                            #send response message
                            response = {
                                "sender_id": "UR_ARM_1",
                                "event": "PICK_COMPLETE",
                                "payload": {
                                    "status": "fail"
                                }
                            }
                            await websocket.send(json.dumps(response))
                        else:
                            # Run blocking code in executor so event loop can process pings
                            loop = asyncio.get_event_loop()
                            async def action():
                                success = await loop.run_in_executor(executor, run_custom_sequence, sequence_name)
                                status = "success" if success else "fail"
                                print(f"STATUS: {status}")
                                return status

                                # Run action with streaming
                            await run_action_with_streaming(
                                websocket,
                                "UR_ARM_1",
                                action_fn=action,
                                response_event="PICK_COMPLETE",
                            )
                    except json.JSONDecodeError:
                        print("Received invalid JSON message")
                # If this point is reached during connection, we break out of the loop
                break

        except Exception as e:
            attempt += 1
            print(f"WebSocket connection error: {e}")
            if attempt < max_retries:
                print(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                print("Max retries reached. Could not connect to server.")