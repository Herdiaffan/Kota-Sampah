# QA Audit — KOTA BERSIH 3D HD + Low-RAM

Tanggal audit: 18 Oktober 2026.

## Hasil pemeriksaan
- JavaScript inline game, `sw.js`, dan generator tekstur lulus pemeriksaan sintaks Node; `manifest.webmanifest` dan `vercel.json` valid JSON.
- ZIP distribusi diuji ulang setelah atlas diregenerasi; semua entri lolos CRC pada pemeriksaan paket akhir.
- Ketiga atlas City/Props/Waste memiliki berkas 1024×1024, 2048×2048, dan 4096×4096. Semua sembilan PNG dapat dibuka. Atlas 4096 diregenerasi dari tekstur prosedural material; atlas 2048 dan 1024 dibuat dengan downsample dari sumber resolusi tinggi yang sama. Perbandingan piksel menunjukkan kedua ukuran rendah cocok persis dengan hasil downsample yang dihasilkan generator; membandingkan atlas 4096 dengan atlas 1024 yang diperbesar menghasilkan MAE sekitar 6,5–7,0, menandakan adanya detail halus yang tidak tersedia pada versi rendah.
- Paket memiliki 10 aset audio Ogg lokal, ikon SVG, manifest, service worker, panduan peluncuran Windows, dan konfigurasi deployment. HTML tidak memakai CDN atau library 3D eksternal.
- Harness Chromium dengan WebGL mock berjalan tanpa exception JavaScript dan tanpa `pageerror`/`console.error`. Peringatan tekstur pada harness sengaja muncul karena pemuatan atlas dinonaktifkan agar tes logika tetap deterministik; sembilan PNG diverifikasi terpisah.
- UI: 7 panel utama terbuka dan tertutup; panel misi menampilkan 15 misi, statistik menampilkan 12 pencapaian; pengaturan grafis/volume tersimpan; pause/resume berfungsi.
- Dunia: 68 titik sampah dan 7 tempat pemilahan; 18 seed menghasilkan 18 tata letak berbeda, 68 posisi unik per dunia, koordinat dalam batas, dan memenuhi kuota kategori minimal yang dibutuhkan misi/resep. Peta menampilkan 6 distrik dan perjalanan cepat berfungsi untuk distrik yang sudah terbuka.
- Kontrol: keyboard berjalan maju, strafing kanan mengubah posisi dan siklus gait, joystick menyentuh menggerakkan karakter, drag kamera mengubah yaw, dan tombol pickup HP memulai aksi yang sama.
- Gameplay: pickup selesai sekali dan tidak dapat menghitung sampah yang sama dua kali; kategori salah ditolak; pemilahan benar menambah stok material; resep memakai bahan yang cukup, tidak dapat dibuat tanpa stok; penjualan mengosongkan produk dan tidak membayar dua kali; upgrade tas menaikkan kapasitas; Eco-Vacuum menyapu sampah dekat dan mengurangi 35 energi; misi/event/tantangan harian memberi hadiah sekali; save v4 terserialisasi termasuk world seed.
- Banner event diperbarui oleh fungsi HUD khusus sehingga tidak ditimpa render loop. Service worker mengecualikan atlas 2048/4096 dari Cache Storage dan hanya memprioritaskan atlas 1024 untuk LOW.

## Konfigurasi grafis
- LOW: atlas 1024, render scale 1×, tanpa antialiasing/bayangan/blur/vignette, jarak sampah lebih pendek, serta jumlah NPC/dekorasi tambahan terbatas. Ini pilihan aman untuk laptop RAM 4 GB.
- MEDIUM: atlas 2048 jika didukung GPU.
- HIGH: mencoba atlas 4096 jika `MAX_TEXTURE_SIZE` GPU ≥4096; otomatis turun ke 2048 jika tidak.
- Browser yang melaporkan RAM ≤4 GB atau tidak melaporkannya memulai pada LOW untuk mengutamakan kestabilan.

## Batasan
- Tes interaksi dijalankan dalam Chromium dengan WebGL mock, bukan GPU/driver sungguhan. Ini menguji DOM, kontrol, alur gameplay dan ketahanan logika, tetapi bukan hasil render shader/tekstur sesungguhnya.
- FPS nyata, penggunaan RAM/GPU, playback audio, Service Worker offline, dan launcher PowerShell harus tetap dicek di laptop Windows target. Tidak ada klaim bahwa FPS tertentu sudah terjamin.

## Tes akhir yang disarankan
1. Ekstrak ZIP ke folder baru dan jalankan `START_WINDOWS.bat`.
2. Biarkan preset **LOW · RAM 4 GB** aktif.
3. Tekan F3, uji gerak maju/samping, pickup, pemilahan, resep, penjualan, toko, peta, audio, dan mainkan setidaknya 3–5 menit.
4. Jika ada aset hilang, layar fatal, audio gagal, atau FPS turun, simpan screenshot dan pesan error untuk tindak lanjut.
