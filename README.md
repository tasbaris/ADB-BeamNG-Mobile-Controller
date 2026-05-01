# ADB BeamNG Mobile Controller 🏎️📱

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/) [![BeamNG](https://img.shields.io/badge/BeamNG.drive-v0.31%2B-orange.svg)](https://www.beamng.com/)
[![Python](https://img.shields.io/badge/python-3.10%2B-brightgreen.svg)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Status](https://img.shields.io/badge/status-stable-success.svg)]()

A professional, ultra-low latency mobile steering wheel and pedal controller for BeamNG.drive. Turn your smartphone into a high-precision virtual racing wheel with support for street driving (clutch) and rally racing (handbrake).

---

## 🇹🇷 Türkçe Kurulum Rehberi

Bu proje, akıllı telefonunuzun jiroskop ve dokunmatik ekranını kullanarak BeamNG.drive'ı kontrol etmenizi sağlar.

### 🚀 Özellikler

- **Ultra Düşük Gecikme:** 10ms döngü süresi ile anında tepki.
- **Çift Mod:** Sokak (Debriyajlı) ve Ralli (El Frenli) arayüzleri.
- **Çoklu Dokunmatik:** Gaz, fren ve viteslere aynı anda basabilme.
- **Sanal Cihaz:** Oyun tarafından gerçek bir direksiyon seti olarak algılanır.
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

1. **Lua Uzantısı:** Oyunda "Open User Folder" diyerek kullanıcı klasörünüzü açın. Eğer yoksa `lua/ge/extensions/` klasörlerini manuel olarak oluşturun ve `mobileController.lua` dosyasını içine kopyalayın.
2. **Arayüz Sunucusunu Başlatın:** Proje klasöründe (index.html'in olduğu yerde) terminali açın ve web arayüzü için şu komutu çalıştırın:

   ```bash
   python3 -m http.server 8000
   ```

3. **Bridge Sunucusunu Başlatın:** Yeni bir terminal sekmesi açın ve köprü sunucusunu başlatın:

   ```bash
   python server.py
   ```

4. **Telefondan Bağlanın:** Tarayıcınızdan (Chrome önerilir) `http://localhost:8000` adresini açın.
5. **Oyunda Tanıtın:**
   - BeamNG konsoluna (`~`) `extensions.load("mobileController")` yazın.
   - **Options > Controls** sekmesinde eksenleri (Direksiyon, Gaz, Fren vb.) telefonunuzu hareket ettirerek tanıtın.

---

## 🇺🇸 English Setup Guide

This project allows you to control BeamNG.drive using your smartphone's gyroscope and touchscreen.

### 🚀 Features

- **Ultra-Low Latency:** 10ms processing loop for instant feedback.
- **Dual Modes:** Street (with Clutch) and Rally (with Handbrake) layouts.
- **Multi-Touch:** Support for simultaneous pedal and gear inputs.
- **Virtual Device:** Recognized as a native steering wheel by BeamNG.
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

1. **Lua Extension:** In-game, click "Open User Folder". If the directories don't exist, create `lua/ge/extensions/` manually, and copy `mobileController.lua` into it.
2. **Start Web Server:** Open a terminal in the project folder (where index.html is located) and run:

   ```bash
   python3 -m http.server 8000
   ```

3. **Start Bridge Server:** Open a new terminal tab and run:

   ```bash
   python server.py
   ```

4. **Connect Mobile:** Open `http://localhost:8000` in your mobile browser (Chrome recommended).
5. **In-Game Setup:**
   - Open BeamNG console (`~`) and type `extensions.load("mobileController")`.
   - Go to **Options > Controls** and bind your axes by moving your phone and pressing the pedals.

---

## 📂 Project Structure

- `index.html`: The mobile web interface with sensor & touch logic.
- `server.py`: Python bridge server (WebSocket to UDP).
- `mobileController.lua`: BeamNG.drive Game Engine extension.

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
