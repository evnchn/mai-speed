# mai-speed
Image loading speedup for https://maimaidx-eng.com/

# DEMO
Left: normal, Right: mai-speed

![mai-speed VS vanilla](demo_gif/newout.gif)

For vanilla, the images takes time to load, and the button layout depends on the dimensions of the image. A shifting layout is not very user-friendly and feels slow. 

A sidenote is that, buttons do work evey if they do not show up _but only for mai-speed since the browsers gets the dimensions of the buttons from the cached image._ For vanilla, buttons could be zero pixel tall during loading. 

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

--> Result: it is a mixed bag. Some browsers consider this as an instruction to never cache and fetch the latest photo from their server. 

Cache-Control header sent by mai-speed.evnchn.io: `Cache-Control: public, immutable, max-age=3600, stale-while-revalidate=600, stale-if-error=259200`

--> Result: most browsers understand the resource is `immutable`, and serve the photo from disk/memory cache with no revalidation. 

This is in addition to Cloudflare hardware

# What's wrong with some browsers? Why so many commits
I was trying to use Cloudflare tunnels, but after using it, caching doesn't work, but it works using localhost for testing. 

Those browser will send 304 before displaying image, instead of skipping requests and serving from cache. 

As shown in demo, mai-speed works on a particular installation of Samsung Internet. Therefore, if it doesn't work, it is the browser's problem. 

---
![StarBurst](https://media.tenor.com/U_Qt6y6AFAYAAAAC/stream-syrex.gif)

_Co-listed as a StarBurst project_
