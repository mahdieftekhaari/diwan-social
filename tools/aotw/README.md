# هنرمند هفته: ساخت پست هفتگی

Builds the «هنرمند هفته» card (and optionally the whole intro deck) for
Instagram (1080x1350), Telegram (1280x720), X (1600x900) and the
Instagram story (1080x1920).

## Weekly use
1. Fill `week.json` (name, activity line, work title) and put the winner's
   `assets/avatar.jpg` (square, 512px) and `assets/cover.jpg` (square).
2. `python3 build.py card`  -> `out/s01_{ig,tg,x,st}.png`
3. `python3 build.py`       -> the full 4-slide intro deck (first week only).

Requires Python 3 + Playwright (chromium). Run from this folder.
Full playbook: project doc «weekly-artist-post-playbook» in the diwan Project.
