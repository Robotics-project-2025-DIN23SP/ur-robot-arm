import asyncio
import cv2
import json
import base64
from .wrist_camera_frame import get_processed_frame

# streaming State
latest_frame = None
streaming_active = False

# get current wrist camera frame
async def frame_provider():
    try:
        loop = asyncio.get_event_loop()
        frame = await loop.run_in_executor(None, get_processed_frame)
        return frame
    except Exception as e:
        print(f"Frame Provider ERROR: {e}")

# JPEG encode
def encode_jpeg(frame):
    try:
        ok, jpg = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
        if not ok:
            return None
        return base64.b64encode(jpg).decode("utf-8")
    except Exception as e:
        print(f"JPEG Encoding ERROR: {e}")


# Capturer Task
async def frame_capturer():
    try:
        global latest_frame, streaming_active

        while streaming_active:
            frame = await frame_provider()
            if frame is not None:
                latest_frame = frame
            await asyncio.sleep(0.001)
    except Exception as e:
        print(f"Frame Capturing ERROR: {e}")


# Sender Task
async def frame_sender(websocket, robot_id):
    try: 
        global latest_frame, streaming_active

        while streaming_active:
            frame = latest_frame
            if frame is not None:
                jpeg_b64 = encode_jpeg(frame)
                if jpeg_b64:
                    await websocket.send(json.dumps({
                        "sender_id": robot_id,
                        "event": "VIDEO_FRAME",
                        "payload": {"image": jpeg_b64}
                    }))
            await asyncio.sleep(0.07)
    except Exception as e:
        print(f"Frame Sending ERROR: {e}")


# Streaming Start/Stop
async def start_streaming(websocket, robot_id):
    try:
        global streaming_active
        streaming_active = True

        capturer = asyncio.create_task(frame_capturer())
        sender = asyncio.create_task(frame_sender(websocket, robot_id))

        print(f"[{robot_id}] Streaming started")
        return capturer, sender
    except Exception as e:
        print(f"Start Frame Streaming ERROR: {e}")


async def stop_streaming(capturer, sender):
    try: 
        global streaming_active
        streaming_active = False

        # Stop tasks
        capturer.cancel()
        sender.cancel()

        await asyncio.gather(capturer, sender, return_exceptions=True)
        print("Streaming stopped")
    except Exception as e:
        print(f"Stop Frame Streaming ERROR: {e}")

# Action + Streaming Integration
async def run_action_with_streaming(
    websocket,
    robot_id,
    action_fn,
    response_event
):
    try: 
        # Start streaming
        capturer_task, sender_task = await start_streaming(
            websocket, robot_id
        )

        # Run action
        status = await action_fn()

        # Stop streaming
        await stop_streaming(capturer_task, sender_task)

        # Send result
        await websocket.send(json.dumps({
            "sender_id": robot_id,
            "event": response_event,
            "payload": {"status": status}
        }))

        
    
    except Exception as e:
        print(f"Run Action With Streaming Frame ERROR: {e}")