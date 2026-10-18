# KOTA BERSIH 3D — Local Windows Setup

## Menjalankan di laptop Windows
1. Unduh ZIP lalu klik kanan → **Extract All / Ekstrak Semua**. Jangan jalankan langsung dari dalam ZIP.
2. Buka folder hasil ekstraksi.
3. Klik dua kali `START_WINDOWS.bat`. Launcher memakai PowerShell bawaan Windows dan membuka Chrome.
4. Pastikan alamat yang terbuka adalah `http://127.0.0.1:8765`. Biarkan jendela server tetap terbuka saat bermain.
5. Pada menu game, pertahankan preset **LOW · RAM 4 GB**. Bayangan, blur, vignette dan antialiasing nonaktif. Target frame pacing 30 FPS; FPS aktual tetap bergantung pada GPU/driver.
6. Tekan **F3** saat bermain untuk menampilkan monitor FPS. Untuk berhenti, tekan Ctrl+C pada jendela server.

## Fitur gameplay
- Enam distrik, 15 misi utama, 12 pencapaian, tantangan harian, inventaris, toko upgrade, peta mini dan penyimpanan progres.
- Pilah sampah lalu olah tujuh jenis produk daur ulang dan jual produk di stasiun pusat.
- Kontrak event bergilir aktif selama 36 detik setiap 110 detik; banner memperlihatkan kemajuan. Pickup beruntun memberi bonus pada setiap combo kelipatan lima.
- Animasi pemain membedakan gerak maju/mundur dan menyamping; pejalan kaki juga mengayun kaki dan tangan.

## Aset dan performa
Paket menyertakan atlas 1024, 2048, dan 4096, audio lokal, ikon, dan launcher. Preset LOW hanya meminta tekstur 1024; MEDIUM memakai 2048; HIGH mencoba 4096 bila GPU mendukung, atau otomatis turun ke 2048. Atlas HD tidak ikut dimuat pada preset LOW. Tidak dibutuhkan Godot, Python, Node.js, atau koneksi internet setelah file diekstrak.

## Batasan
- Windows 10/11, Chrome atau Edge modern dengan WebGL aktif.
- Game tetap website lokal di browser, bukan executable native `.exe`.
- Kualitas render akhir dan FPS aktual belum diuji pada GPU laptop pengguna; pengujian logika tidak dapat menjamin kestabilan 30 FPS pada semua perangkat.
