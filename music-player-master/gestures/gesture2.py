import cv2
import mediapipe as mp
import asyncio
import websockets
import json
import threading

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# WebSocket server setup
connected_clients = set()

async def websocket_handler(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            pass  # No need to receive messages, only send
    finally:
        connected_clients.remove(websocket)

async def send_gesture(gesture):
    if connected_clients:
        message = json.dumps({"gesture": gesture})
        await asyncio.wait([client.send(message) for client in connected_clients])

def detect_gestures():
    cap = cv2.VideoCapture(0)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Extract key landmark positions
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                
                # Gesture detection logic
                if thumb_tip.y < index_tip.y and thumb_tip.y < middle_tip.y:
                    gesture = "volume_up"
                elif thumb_tip.y > index_tip.y and thumb_tip.y > middle_tip.y:
                    gesture = "volume_down"
                elif index_tip.x < middle_tip.x:  # Swipe left
                    gesture = "previous"
                elif index_tip.x > middle_tip.x:  # Swipe right
                    gesture = "next"
                else:
                    gesture = "play_pause"
                
                asyncio.run(send_gesture(gesture))
        
        cv2.imshow("Gesture Control", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

def run_camera():
    detect_gestures()  # Runs the OpenCV gesture detection

async def main():
    server = await websockets.serve(websocket_handler, "localhost", 8765)
    print("WebSocket Server Started on ws://localhost:8765")
    
    # Run the camera in a separate thread
    camera_thread = threading.Thread(target=run_camera)
    camera_thread.start()
    
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
