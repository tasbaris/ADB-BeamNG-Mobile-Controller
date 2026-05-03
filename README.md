# ADB BeamNG Mobile Controller 🏎️📱

[![Version](https://img.shields.io/badge/version-2.2.0-blue.svg)](https://github.com/) [![BeamNG](https://img.shields.io/badge/BeamNG.drive-v0.31%2B-orange.svg)](https://www.beamng.com/)
[![Python](https://img.shields.io/badge/python-3.10%2B-brightgreen.svg)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Status](https://img.shields.io/badge/status-stable-success.svg)]()

A professional, ultra-low latency mobile steering wheel and pedal controller for BeamNG.drive. Turn your smartphone into a high-precision virtual racing wheel with a live telemetry dashboard, support for street driving (clutch) and rally racing (handbrake).

### Screenshot
Normal Dash
![BeamNG Mobile Controller](dash.jpeg)

F1/GT3 Dash
![BeamNG Mobile Controller](f1.jpeg)


Race Dash(just for telemetry)
![BeamNG Mobile Controller](race_dash.png)

---

## 🇹🇷 Türkçe Kurulum Rehberi

Bu proje, akıllı telefonunuzun jiroskop ve dokunmatik ekranını kullanarak BeamNG.drive'ı kontrol etmenizi ve canlı araç verilerini (hız, devir, vites) ekranınızda görmenizi sağlar.

### 🚀 Özellikler

- **✨ Çift Arayüz Modu (Dual UI):** F1 tarzı profesyonel direksiyon (`f1_wheel.html`) ile Klasik ergonomik mod (`index.html`) arasında tek tuşla geçiş.
- **🧠 Otomatik RPM Kalibrasyonu:** Arayüz, aracın limitlerini otomatik öğrenir ve LED göstergeleri buna göre ayarlar.
- **Çift Yönlü Telemetri:** Telefonunuzda RPM, Hız (KM/H), Vites ve Turbo Basıncı gibi verileri anlık gösteren dijital panel (Dinamik Shift Light destekli).
- **Ultra Düşük Gecikme:** 10ms döngü süresi ile anında tepki.
- **Çoklu Dokunmatik:** Gaz, fren ve viteslere aynı anda basabilme. Ergonomik yerleşim ve yeni Gri Debriyaj desteği.
- **Bağımsız GT3 Yarış Ekranı:** İkinci monitörler veya tabletler için ultra detaylı `race_dash.html` MoTeC stili panel.
- **💻 Uyumluluk:** Bu proje macOS üzerinde **CrossOver** kullanılarak test edilmiş ve başarıyla çalıştırılmıştır.

### 🔌 ADB Reverse Kurulumu (Önerilen)

Sensörlerin (jiroskop) çalışması için HTTPS gereksinimini aşmak ve en düşük gecikmeyi sağlamak amacıyla telefonunuzun **Geliştirici Seçeneklerinden "USB Hata Ayıklama"yı** açın ve USB üzerinden şu komutları kullanın:

```bash
# Web arayüzü erişimi için (8000 portu)
adb reverse tcp:8000 tcp:8000

# WebSocket iletişimi için (8765 portu)
adb reverse tcp:8765 tcp:8765

```

### 🛠️ Kurulum

1. **OutGauge'u Etkinleştirin (Telemetri İçin ŞARTTIR):**
   - BeamNG.drive'da **Options (Ayarlar) > Other (Diğer)** sekmesine gidin.
   - **OutGauge support** kutucuğunu işaretleyin.
   - **IP** adresini `127.0.0.1` ve **Port** numarasını `4444` yapın.
2. **Lua Uzantısı:** Oyunda "Open User Folder" diyerek kullanıcı klasörünüzü açın. Eğer yoksa `lua/ge/extensions/` klasörlerini manuel olarak oluşturun ve `mobileController.lua` dosyasını içine kopyalayın.
3. **Arayüz Sunucusunu Başlatın:** Proje klasöründe (index.html'in olduğu yerde) terminali açın ve web arayüzü için şu komutu çalıştırın:

   ```bash
   python3 -m http.server 8000
   ```

4. **Bridge Sunucusunu Başlatın:** Yeni bir terminal sekmesi açın ve köprü sunucusunu başlatın:

   ```bash
   python server.py
   ```

5. **Telefondan Bağlanın:** Tarayıcınızdan (Chrome önerilir) `http://localhost:8000` adresini açın.
6. **Oyunda Tanıtın:**
   - BeamNG konsoluna (`~`) `extensions.load("mobileController")` yazın.
   - **Options > Controls** sekmesinde eksenleri (Direksiyon, Gaz, Fren vb.) telefonunuzu hareket ettirerek tanıtın.

> **Not:** Ayrı olan gelişmiş GT3 yarış ekranını başlatmak isterseniz `python race_server.py` komutunu çalıştırıp `http://localhost:8000/race_dash.html` adresine gidebilirsiniz.

---

## 🇺🇸 English Setup Guide

This project allows you to control BeamNG.drive using your smartphone's gyroscope and touchscreen while displaying live telemetry data directly on your screen.

### 🚀 Features

- **✨ Dual Interface Mode:** Instantly switch between the new F1-style professional wheel (`f1_wheel.html`) and the Classic ergonomic mode (`index.html`) with a single tap.
- **🧠 Auto RPM Calibration:** Automatically learns the vehicle's max RPM and adjusts LED scaling accordingly.
- **Bi-Directional Telemetry:** A live digital dash on your phone showing RPM, Speed (KM/H), Gear, and Turbo Boost (with Dynamic Shift Light).
- **Ultra-Low Latency:** 10ms processing loop for instant feedback.
- **Multi-Touch:** Support for simultaneous pedal and gear inputs. Featuring new ergonomic triggers and a top-to-bottom Grey Clutch.
- **Standalone GT3 Dashboard:** Included `race_dash.html` for a detailed MoTeC-style professional screen for tablets or 2nd monitors.
- **💻 Compatibility:** This project has been tested and verified on **macOS** using **CrossOver**.

### 🔌 ADB Reverse Setup (Recommended)

To bypass HTTPS requirements for sensors and ensure minimum latency, enable **"USB Debugging" from your phone's Developer Options**, and use these commands over USB:

```bash
# For Web Interface (Port 8000)
adb reverse tcp:8000 tcp:8000

# For WebSocket Bridge (Port 8765)
adb reverse tcp:8765 tcp:8765

```

### 🛠️ Installation

1. **Enable OutGauge (REQUIRED for Telemetry):**
   - Open BeamNG.drive and go to **Options > Other**.
   - Check the **OutGauge support** box.
   - Ensure **IP** is set to `127.0.0.1` and **Port** is `4444`.
2. **Lua Extension:** In-game, click "Open User Folder". If the directories don't exist, create `lua/ge/extensions/` manually, and copy `mobileController.lua` into it.
3. **Start Web Server:** Open a terminal in the project folder (where index.html is located) and run:

   ```bash
   python3 -m http.server 8000
   ```

4. **Start Bridge Server:** Open a new terminal tab and run:

   ```bash
   python server.py
   ```

5. **Connect Mobile:** Open `http://localhost:8000` in your mobile browser (Chrome recommended).
6. **In-Game Setup:**
   - Open BeamNG console (`~`) and type `extensions.load("mobileController")`.
   - Go to **Options > Controls** and bind your axes by moving your phone and pressing the pedals.

> **Note:** To start the advanced standalone GT3 racing dashboard, run `python race_server.py` and open `http://localhost:8000/race_dash.html`.

---

## 📂 Project Structure

- `index.html`: The redesigned ergonomic classic mobile web interface.
- `f1_wheel.html`: The new professional F1/GT3 style steering wheel interface.
- `server.py`: Stable Python bridge server (WebSocket to UDP) for the controller.
- `mobileController.lua`: BeamNG.drive Game Engine extension.
- `race_dash.html` & `race_server.py`: Standalone professional GT3 racing dashboard.
- `outgauge_tester.py`: CLI tool for testing raw telemetry data.

---

## ⚠️ Requirements / Gereksinimler

- **Python:** 3.10 or higher
- **Library:** `pip install websockets`
- **Network:** USB Debugging (ADB Reverse)

---

## 📄 License

This project is licensed under the **MIT License**.

```text
MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```