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

# Why does it work
Cache-Control header sent by maimaidx-eng.com: `Cache-Control: max-age=864000; Cache-Control: no-cache`

Cache-Control header sent by mai-speed.evnchn.io: `Cache-Control: public, immutable, max-age=3600, stale-while-revalidate=600, stale-if-error=259200`

This is in addition to Cloudflare hardware

# What's wrong with some browsers?
It always want to cache the images, and then browser will send 304 before displaying image, instead of skipping requests and serving from cache. 

mai-speed works on a particular installation of Samsung Internet. Therefore, if it doesn't work, it is the browser problem. 

---
![StarBurst](https://media.tenor.com/U_Qt6y6AFAYAAAAC/stream-syrex.gif)

_Co-listed as a StarBurst project_
