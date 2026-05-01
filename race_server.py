import asyncio
import websockets
import socket
import struct
import time

# --- CONFIGURATION ---
WS_HOST = "0.0.0.0"
WS_PORT = 8765

OUTGAUGE_LISTEN_IP = "0.0.0.0"
OUTGAUGE_LISTEN_PORT = 4444  

# --- SOCKET SETUP ---
telemetry_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    telemetry_sock.bind((OUTGAUGE_LISTEN_IP, OUTGAUGE_LISTEN_PORT))
    telemetry_sock.setblocking(False)
except OSError:
    print(f"[!] HATA: UDP {OUTGAUGE_LISTEN_PORT} portu zaten kullanımda!")
    print(" Lütfen 'server.py'yi durdurun. Aynı anda tek bir OutGauge dinleyicisi çalışabilir.")
    exit(1)

connected_clients = set()

async def ws_handler(websocket):
    """Bağlanan telefonlara telemetriyi iletir."""
    connected_clients.add(websocket)
    client_addr = websocket.remote_address[0]
    print(f"\n[OK] Yarış Ekranı bağlandı: {client_addr}")
    try:
        async for message in websocket:
            pass 
    except websockets.exceptions.ConnectionClosed:
        print(f"\n[!] Yarış Ekranı ayrıldı: {client_addr}")
    finally:
        connected_clients.remove(websocket)

async def telemetry_loop():
    loop = asyncio.get_event_loop()
    print(f"[*] Telemetri Dinleniyor: UDP {OUTGAUGE_LISTEN_PORT}")
    
    while True:
        try:
            data, addr = await loop.run_in_executor(None, telemetry_sock.recvfrom, 1024)
            if len(data) >= 92:
                # Format: <I4sHbbfffffffIIfff16s16si
                outgauge = struct.unpack('<I4sHbbfffffffIIfff16s16si', data)
                gear = outgauge[3] # 0:R, 1:N, 2:1st...
                speed = outgauge[5] * 3.6
                rpm = outgauge[6]
                turbo = outgauge[7]
                engTemp = outgauge[8]
                fuel = outgauge[9] * 100
                oilPress = outgauge[10]
                oilTemp = outgauge[11]
                dashLights = outgauge[13] # showLights
                throttle = outgauge[14] * 100
                brake = outgauge[15] * 100
                clutch = outgauge[16] * 100
                
                # Payload Format
                payload = f"T|{speed:.0f}|{rpm:.0f}|{gear}|{engTemp:.0f}|{oilTemp:.0f}|{oilPress:.1f}|{fuel:.0f}|{turbo:.2f}|{throttle:.0f}|{brake:.0f}|{clutch:.0f}|{dashLights}"
                
                if connected_clients:
                    await asyncio.gather(*[c.send(payload) for c in connected_clients], return_exceptions=True)
        except Exception:
            await asyncio.sleep(0.01)
            continue
        await asyncio.sleep(0.01) # 100Hz update

async def main():
    print("="*60)
    print(" BEAMNG GT3 YARIŞ EKRANI (DASHBOARD) SUNUCUSU")
    print(f" Web Arayüzü Bağlantı Portu (WS): {WS_PORT}")
    print("="*60)
    
    async with websockets.serve(ws_handler, WS_HOST, WS_PORT):
        await telemetry_loop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSunucu kapatılıyor...")