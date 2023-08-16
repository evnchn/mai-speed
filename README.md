# mai-speed
Image loading speedup for https://maimaidx-eng.com/

# Server endpoint
`https://mai-speed.evnchn.io/{path}` where path is the URL with `https://` removed

such as `https://mai-speed.evnchn.io/maimaidx-eng.com/maimai-mobile/img/Chara/bab779e7ab508427.png`

# Userscript
Check `mai-speed-userscript.js`. Latest version v1.2

# How does this work
1. If not present, download image to `cache` folder
2. Serve the cached version of the image.

# What's wrong with cloudflare
It always want to cache the images, and then browser will send 304 before displaying image, instead of skipping requests and serving from cache. 
**Help is needed.**
