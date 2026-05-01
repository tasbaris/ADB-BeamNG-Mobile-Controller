import asyncio
import websockets
import socket
import time

# UDP Configuration for BeamNG communication
UDP_IP = "127.0.0.1"
UDP_PORT = 5555
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

async def handler(websocket):
    """
    Handles incoming WebSocket connections from the mobile device.
    Forwards received data to BeamNG via UDP.
    """
    print(f"\n[OK] Mobile device connected: {websocket.remote_address}")
    
    try:
        async for message in websocket:
            # Send raw data string directly to the Lua extension's UDP port
            sock.sendto(message.encode('utf-8'), (UDP_IP, UDP_PORT))
                
    except websockets.exceptions.ConnectionClosed:
        print("\n[!] Connection lost with mobile device.")
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")

async def main():
    """
    Starts the WebSocket server on port 8765.
    Listens on all interfaces (0.0.0.0) for local network access.
    """
    print("="*60)
    print("BEAMNG MOBILE CONTROLLER BRIDGE SERVER")
    print(f"WebSocket Listening on:  0.0.0.0:8765")
    print(f"UDP Forwarding to:       {UDP_IP}:{UDP_PORT}")
    print("="*60)
    print("Keep this window open while playing.")
    
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer shutting down...")
