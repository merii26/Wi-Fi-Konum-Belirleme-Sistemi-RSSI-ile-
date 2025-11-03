import serial, re, math
from datetime import datetime
from scipy.optimize import minimize

known_aps = {
    "AP1": {"location": (0.0001, 0.0001), "rssi": -60},
    "AP2": {"location": (-0.0001, -0.0001), "rssi": -65},
    "AP3": {"location": (0.0002, -0.0001), "rssi": -55},
}

def calculate_distance(signal_strength, frequency=2400):
    return 10 ** ((27.55 - (20 * math.log10(frequency)) + abs(signal_strength)) / 20)

def trilateration(known_aps, target_rssi):
    def distance_error(location, known_aps, target_rssi):
        err = 0
        for ap_name, ap_info in known_aps.items():
            loc = ap_info["location"]
            ref_rssi = ap_info["rssi"]
            d1 = calculate_distance(ref_rssi)
            d2 = calculate_distance(target_rssi)
            err += (math.dist(location, loc) - abs(d1 - d2)) ** 2
        return err

    res = minimize(distance_error, (0,0), args=(known_aps, target_rssi), method='L-BFGS-B')
    return res.x

# Windows için COM3, macOS/Linux için /dev/ttyUSB0 olabilir
ser = serial.Serial("COM8", 115200, timeout=1)

while True:
    line = ser.readline().decode("utf-8", "ignore").strip()
    m = re.search(r"SSID: (.+) RSSI: (-?\d+)", line)
    if m:
        ssid = m.group(1)
        rssi = int(m.group(2))
        if rssi > -50:
            est = trilateration(known_aps, rssi)
            dist = calculate_distance(rssi)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {ssid} → RSSI: {rssi} dBm, "
                  f"Dist≈{dist:.2f} m, Loc={est}")