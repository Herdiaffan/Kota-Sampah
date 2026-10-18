# Changelog — KOTA BERSIH 3D

## 18 Oktober 2026 — Audit performa dan kualitas grafis
- Memvalidasi nilai preset grafis dari save lama; nilai tak dikenal kembali ke LOW. Volume audio dibatasi pada rentang 0–1.
- Perubahan LOW/MEDIUM/HIGH sekarang membangun ulang geometri statis agar detail kota ikut berubah, bukan hanya mesh dinamis. Buffer statis lama dihapus sebelum buffer baru dibuat.
- Preset LOW pada perangkat RAM rendah memakai atlas 1024 px, tanpa antialiasing, target 30 FPS, dekorasi tambahan dikurangi, dan tanpa bayangan/blur/vignette.
- Cache Service Worker dinaikkan ke v16 agar file baru tidak tertahan cache versi sebelumnya.
- Audit otomatis fungsi gameplay dan struktur: 28/28 pemeriksaan pada harness dengan WebGL mock lulus.
- Pencatatan batasan: rendering visual/WebGL dan FPS aktual tidak dapat diuji pada GPU nyata dari lingkungan build ini.

## 2026-10-18 — Directional walking animation fix
- Replaced the subtle time-only leg sway with a movement-synchronised gait.
- Added alternating foot lift and forward/back stride, plus lateral foot placement for strafing.
- Added opposing arm swing, a small upper-body bounce, and separate run cadence.
- Animation direction is derived from the actual movement vector so keyboard and on-screen joystick use the same logic.
- Kept the low-memory renderer and shadow-free policy unchanged. JavaScript syntax checked with Node; actual GPU FPS still depends on the user's laptop/browser.


## 18 Oktober 2026 — Gameplay & replayability pass
- Added five rotating timed event contracts (cleanup, plastics, e-waste, sorting, and organic waste), each with visible progress, a 36-second window, and CR/PTS/XP rewards.
- Added milestone payouts at combo ×5, ×10, etc.; a fresh session starts a fresh combo chain so old saved timestamps cannot inflate a new run.
- NPC pedestrians now animate their steps and arm swings instead of sliding with fixed legs.
- Event completion feedback is emitted after ordinary pickup/sorting messages so the reward toast remains visible.
- Capped the shipped texture selection at 2048 px for HIGH as well as MEDIUM. LOW stays at 1024 px; this keeps the package smaller and avoids oversized texture uploads on a 4 GB system while retaining detailed textures.


## 18 Oktober 2026 — HD assets + LOW-RAM split
- Paket distribusi kembali memenuhi permintaan ukuran 100 MB+ dengan tiga atlas 4096×4096 yang dipakai preset HIGH pada perangkat yang mampu menjalankannya.
- LOW tetap memuat hanya atlas 1024×1024 untuk laptop RAM 4 GB; tidak sekadar memuat atlas besar lalu mengabaikannya.
- HIGH memilih 4096 hanya saat GPU melaporkan dukungan tekstur 4096; jika tidak, turun ke 2048.
- Service Worker tidak menyimpan atlas 2048/4096 ke Cache Storage agar HD tidak menghabiskan ruang cache.
- Service Worker cache namespace bumped to v18 so browsers refresh HTML and cache-policy changes cleanly.

## 18 Oktober 2026 — Regenerasi tekstur & audit runtime akhir
- Regenerated all three 4096×4096 material atlases from the procedural texture source, then derived their 2048 and 1024 variants from those same sources so the resolutions stay consistent and the HD versions retain fine surface detail.
- Reran the Chromium interaction harness against the final app code: primary panels, movement/strafe gait, mobile joystick/camera/pickup, recycling workshop, recipes, sale guards, upgrades/Eco-Vacuum, missions, timed-event rewards, daily claim and save serialization.
- Reran 18 seeded-world layouts; each generated 68 unique trash positions with category quotas satisfied.
- Confirmed that in-game 3D GPU rendering and FPS are still not certifiable from a WebGL-mock harness; the final visual check remains a laptop-side step.
