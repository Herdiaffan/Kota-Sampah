# Status — KOTA BERSIH 3D, Replayability / Low-RAM update

## Gameplay
- WebGL 3D procedural city, third-person character, directional walking/running/strafe gait and pickup animation.
- Six districts, seeded layout of 68 starting trash items, category sorting, seven recycling recipes, product sales, 15 main missions, upgrades, daily challenge, 12 achievements, save/load, district map/fast travel and PC/touch controls.
- Five rotating 36-second event contracts with progress tracking and rewards; 1.5x score event bonus; combo rewards at multiples of five; pedestrians animate their legs and arms.
- Audio ambience and sound effects are local assets; game uses no external 3D/CDN libraries.

## RAM and graphics
- Shadows, blur, vignette and antialiasing are disabled. LOW uses 1024 px atlases, render scale 1x and 30 FPS target; MEDIUM uses 2048 px atlases; HIGH requests 4096 px if GPU support permits and falls back to 2048 when it does not.
- LOW preset is forced when browser RAM is 4 GB or unknown. Object/NPC/detail distances are reduced on LOW.

## QA status
- Inline JavaScript, service worker, texture generator, JSON configuration and referenced local assets are checked in the final build. A Chromium DOM/gameplay harness with WebGL mock passes interaction checks; texture images are separately validated.
- Logic/runtime harness covers collection/no-duplicate, sorting, recipe economics, time-limited event rewards, upgrade and vacuum guards, save version, mission bounds, all primary dialogs, PC/mobile movement, 18 world seeds and content construction.
- **GPU visual quality and actual FPS cannot be certified here**; run Chrome on the target laptop and use F3 to read the local FPS counter.


Paket HD-LowRAM: atlas 1024/2048/4096 disertakan; seluruh atlas diregenerasi dari satu sumber prosedural high-detail dan divalidasi dimensinya. RAM 4 GB tetap memakai preset LOW/1024; atlas 4096 hanya dipilih pada preset HIGH jika GPU mendukung 4096.
