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

# Create a thread pool for blocking operations
executor = ThreadPoolExecutor(max_workers=1)

async def websocket_connection():
    async with websockets.connect(URL) as websocket:
        print("connecting to server")

        # send init message
        init_msg = {
            "sender_id": "UR_ARM_1",
            "event": "INIT",
            "payload": {
                "token": SECRET_TOKEN, 
                "role": "ROBOT"
            }
        }
    
        await websocket.send(json.dumps(init_msg)) 

        # listen for messages
        async for message in websocket:
            message_data = json.loads(message)
            event = message_data.get("event")
            payload = message_data.get("payload", {})

            print(f"EVENT: {event}")

            if event == "CONNECTED":
                print("server is connected")
            elif event == "PICK_AND_PLACE" or "TEST_PICK_AND_PLACE":
                # get code for ordered product 

                # TODO: FIX ERROR!
                # Error description:
                # If a wrong product (like P005) is given, we get the error
                # under "if not sequence_name:". As soon as the error is done calling,
                # the code continues to the "else" block and picks up item_1 

                product_code = payload.get("product", "P001")
                print(f"Payload: {payload}")
                sequence_name = PRODUCT_TO_SEQUENCE.get(product_code)
                print(f"Sequence_name: {sequence_name}")

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