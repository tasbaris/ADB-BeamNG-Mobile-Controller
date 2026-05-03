import asyncio
import websockets
import time
import math

async def handler(websocket, path=None):
    print("İstemci (Tarayıcı) bağlandı!")
    start_time = time.time()
    try:
        while True:
            # Client'tan gelen mesajı da non-blocking okumak için wait_for kullanabiliriz,
            # Ama basit bir test server'ı olduğu için asenkron gönderimi öncelikli yapalım.
            try:
                msg = await asyncio.wait_for(websocket.recv(), timeout=0.015)
                # Gelen veriyi yazdırabiliriz: print(f"Gelen: {msg}")
            except asyncio.TimeoutError:
                pass # 15ms içinde mesaj gelmezse devam et
            
            t = time.time() - start_time
            
            # Sahte Telemetri Verisi Üretimi
            speed = int(abs(math.sin(t * 0.1)) * 320)  # 0-320 km/h arası dalgalanma
            rpm = int(abs(math.sin(t * 0.5)) * 8000)   # 0-8000 rpm arası dalgalanma
            gear = int((t % 6) + 1)                    # 1'den 6'ya kadar vites (0: R, 1: N, 2: 1. vites vb. index.html mantığında)
            
            flags = 0
            if rpm > 7500:
                flags |= 256  # Check Engine
            if speed > 200:
                flags |= 16   # ESC
                
            turbo = abs(math.sin(t * 0.2)) * 2.5
            fuel = int(100 - (t % 100)) # 100'den geriye sayım
            eng = 90 + int(math.sin(t * 0.1) * 20)
            oil = 95 + int(math.sin(t * 0.1) * 25)
            
            # Format: T|Speed|RPM|Gear|Flags|Turbo|Fuel|EngTemp|OilTemp
            telemetry = f"T|{speed}|{rpm}|{gear}|{flags}|{turbo:.2f}|{fuel}|{eng}|{oil}"
            
            await websocket.send(telemetry)
            await asyncio.sleep(0.015) # 60 FPS / ~15ms
            
    except websockets.exceptions.ConnectionClosed:
        print("İstemci bağlantısı koptu.")

async def main():
    print("Mock Server başlatılıyor: ws://0.0.0.0:8765")
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()  # Sonsuza kadar çalış

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Sunucu durduruldu.")