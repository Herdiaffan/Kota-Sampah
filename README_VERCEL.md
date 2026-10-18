# Deploy KOTA BERSIH 3D ke Vercel

## Isi paket
`index.html` berada di root proyek, disertai `vercel.json`, `sw.js`, `manifest.webmanifest`, audio, ikon, dan enam atlas tekstur 1024/2048. Ini website statis tanpa build command dan tanpa framework eksternal.

## Deploy
1. Ekstrak ZIP ke komputer agar bisa memeriksa struktur file.
2. Buat proyek baru di Vercel dan unggah folder proyek, atau deploy melalui integrasi Git.
3. Pastikan `index.html` menjadi entry point, lalu buka URL hasil deployment.

## Optimasi
- Tidak ada shadow map, shadow pass, contact shadow, CSS shadow, blur, vignette atau antialiasing.
- LOW memakai atlas 1024, render scale 1×, target frame pacing 30 FPS, serta mengurangi jumlah NPC/dekorasi dan jarak objek.
- MEDIUM/HIGH memakai maksimal atlas 2048 agar paket dan beban memori lebih terkendali.
- Event contracts, combo rewards, misi, penyimpanan progres dan audio lokal tidak memerlukan backend.
- FPS aktual perlu diuji pada perangkat target.
