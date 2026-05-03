import asyncio
import websockets
import socket
import struct
import time

# --- CONFIGURATION ---
WS_HOST = "0.0.0.0"
WS_PORT = 8765

FORWARD_UDP_IP = "127.0.0.1"
FORWARD_UDP_PORT = 5555  # To mobileController.lua

OUTGAUGE_LISTEN_IP = "127.0.0.1"
OUTGAUGE_LISTEN_PORT = 4444  # From BeamNG Outgauge

# --- SOCKET SETUP ---
# Socket to send commands to BeamNG Lua
cmd_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Socket to receive telemetry from BeamNG
telemetry_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
telemetry_sock.bind((OUTGAUGE_LISTEN_IP, OUTGAUGE_LISTEN_PORT))
telemetry_sock.setblocking(False)

# Global list and active controller tracking
connected_clients = set()
active_controller = None

async def ws_handler(websocket):
    """Handles incoming control data from the mobile device."""
    global active_controller
    connected_clients.add(websocket)
    active_controller = websocket # Set this as the primary controller
    
    client_addr = websocket.remote_address[0]
    print(f"\n[OK] Device connected: {client_addr} | Total: {len(connected_clients)}")
    
    last_log_time = 0
    try:
        async for message in websocket:
            # Only process messages if this is the latest connected device
            # This prevents "flickering" when switching between UI pages
            if websocket != active_controller:
                continue
                
            # Forward controls to Lua extension
            cmd_sock.sendto(message.encode('utf-8'), (FORWARD_UDP_IP, FORWARD_UDP_PORT))
            
            current_time = time.time()
            if current_time - last_log_time >= 0.5:
                print(f"[UI->LUA] {message}")
                last_log_time = current_time
                
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected_clients.remove(websocket)
        if active_controller == websocket:
            active_controller = None
        print(f"\n[!] Device disconnected. Remaining: {len(connected_clients)}")

async def telemetry_loop():
    """Listens for Outgauge packets from BeamNG and broadcasts to all phones."""
    loop = asyncio.get_event_loop()
    print(f"[*] Telemetry listener started on UDP:{OUTGAUGE_LISTEN_PORT}")
    
    while True:
        try:
            # Non-blocking receive
            data, addr = await loop.run_in_executor(None, telemetry_sock.recvfrom, 1024)
            if len(data) >= 92: # Outgauge packet size
                # Unpack Outgauge packet (Simplified selection for the phone)
                # struct OutGaugePack: time, car[4], flags, gear, spare, speed, rpm, turbo, engTemp, fuel, etc.
                # Format: <I4sHbbfffffffIIfff16s16si
                # We need: gear (idx 3), speed (idx 5), rpm (idx 6), turbo (idx 7), showLights (idx 13)
                outgauge_data = struct.unpack('<I4sHbbfffffffIIfff16s16si', data)
                
                gear = outgauge_data[3] # 0: R, 1: N, 2: 1st, 3: 2nd...
                speed = outgauge_data[5] * 3.6 # m/s to km/h
                rpm = outgauge_data[6]
                turbo = outgauge_data[7] # Turbo pressure in Bar
                eng_temp = outgauge_data[8]
                fuel = outgauge_data[9] * 100
                oil_temp = outgauge_data[11]
                dash_lights = outgauge_data[13] # showLights: Bitfield for currently ON warnings
                
                # Format: "T|SPEED|RPM|GEAR|LIGHTS|TURBO|FUEL|ENGTEMP|OILTEMP"
                payload = f"T|{speed:.0f}|{rpm:.0f}|{gear}|{dash_lights}|{turbo:.2f}|{fuel:.0f}|{eng_temp:.0f}|{oil_temp:.0f}"
                
                if connected_clients:
                    # Broadcast to all connected WebSockets
                    # We use wait to not block the loop
                    await asyncio.gather(*[client.send(payload) for client in connected_clients], return_exceptions=True)
        except Exception:
            await asyncio.sleep(0.01) # Small rest if no data
            continue
        await asyncio.sleep(0.01) # ~100Hz max update

async def main():
    print("="*60)
    print("BEAMNG CONTROL - BIDIRECTIONAL SERVER")
    print(f"WS Port (Mobile):    {WS_PORT}")
    print(f"Outgauge (BeamNG):   {OUTGAUGE_LISTEN_PORT}")
    print("="*60)
    
    # Start both server and telemetry loop
    async with websockets.serve(ws_handler, WS_HOST, WS_PORT):
        await telemetry_loop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer shutting down...")
