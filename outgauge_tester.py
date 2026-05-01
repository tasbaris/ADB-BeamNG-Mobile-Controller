import socket
import struct
import time
import os

# --- LFS/BeamNG OutGauge struct format ---
# unsigned time;            // I (4 bytes)
# char car[4];              // 4s (4 bytes)
# unsigned short flags;     // H (2 bytes)
# char gear;                // b (1 byte)
# char plid;                // b (1 byte)
# float speed;              // f (4 bytes)
# float rpm;                // f (4 bytes)
# float turbo;              // f (4 bytes)
# float engTemp;            // f (4 bytes)
# float fuel;               // f (4 bytes)
# float oilPressure;        // f (4 bytes)
# float oilTemp;            // f (4 bytes)
# unsigned dashLights;      // I (4 bytes)
# unsigned showLights;      // I (4 bytes)
# float throttle;           // f (4 bytes)
# float brake;              // f (4 bytes)
# float clutch;             // f (4 bytes)
# char display1[16];        // 16s (16 bytes)
# char display2[16];        // 16s (16 bytes)
# int id;                   // i (4 bytes)
# 
# Total: 92 bytes.
# Format: <I4sHbbfffffffIIfff16s16si

OUTGAUGE_PORT = 4444

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        sock.bind(("0.0.0.0", OUTGAUGE_PORT))
        print(f"[*] Listening: UDP Port {OUTGAUGE_PORT}...")
        print("[!] Note: If 'server.py' is running, a conflict may occur. Please stop 'server.py' first if the port is in use.")
        print("-" * 50)
    except Exception as e:
        print(f"[ERROR] Failed to listen on port {OUTGAUGE_PORT}: {e}")
        print("Please stop 'server.py' first if the port is in use.")
        return

    last_print = 0

    while True:
        try:
            data, addr = sock.recvfrom(1024)
            if len(data) >= 92:
                current_time = time.time()
                
                if current_time - last_print > 0.5:
                    outgauge = struct.unpack('<I4sHbbfffffffIIfff16s16si', data)
                    
                    time_ms = outgauge[0]
                    car_name = outgauge[1].decode('ascii', errors='ignore').strip('\x00')
                    flags = outgauge[2]
                    gear = outgauge[3]
                    plid = outgauge[4]
                    speed = outgauge[5] * 3.6 # m/s -> km/h
                    rpm = outgauge[6]
                    turbo = outgauge[7]
                    engTemp = outgauge[8]
                    fuel = outgauge[9]
                    oilPress = outgauge[10]
                    oilTemp = outgauge[11]
                    dashLights = outgauge[12]
                    showLights = outgauge[13]
                    throttle = outgauge[14]
                    brake = outgauge[15]
                    clutch = outgauge[16]
                    display1 = outgauge[17].decode('ascii', errors='ignore').strip('\x00')
                    display2 = outgauge[18].decode('ascii', errors='ignore').strip('\x00')
                    id_ = outgauge[19]


                    os.system('cls' if os.name == 'nt' else 'clear')
                    
                    print("="*40)
                    print(" BEAMNG OUTGAUGE RAW TELEMETRY")
                    print("="*40)
                    print(f"Vehicle:      {car_name}")
                    print(f"Speed:        {speed:.1f} KM/H")
                    print(f"RPM:          {rpm:.0f}")
                    print(f"Gear (Index): {gear} (0:R, 1:N, 2:1st...)")
                    print(f"Turbo (Bar):  {turbo:.3f} BAR")
                    print(f"Eng Temp:     {engTemp:.1f} °C")
                    print(f"Oil Temp:     {oilTemp:.1f} °C")
                    print(f"Oil Press:    {oilPress:.2f} BAR")
                    print(f"Fuel Level:   {fuel*100:.1f} %")
                    print("-" * 40)
                    print(f"Pedals (Game):")
                    print(f" Throttle:  {throttle:.2f}")
                    print(f" Brake:     {brake:.2f}")
                    print(f" Clutch:    {clutch:.2f}")
                    print("-" * 40)
                    print(f"Dash Lights (Bitmask): {dashLights}")
                    print(f"Show Lights (Bitmask): {showLights}")
                    print(f"Flags (Bitmask):       {flags}")
                    print("="*40)
                    
                    last_print = current_time
                    
        except KeyboardInterrupt:
            print("\Exiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()