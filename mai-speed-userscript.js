// ==UserScript==
// @name         mai-speed
// @namespace    https://mai-speed.evnchn.io
// @version      1.1
// @description  Apply image caching for faster loading
// @match        https://maimaidx-eng.com/*
// @match        http://maimaidx-eng.com/*
// @run-at       document-body
// ==/UserScript==




(function () {
    'use strict';
    console.log("mai-speed start!");
    localStorage.setItem("mai-speed-server-status", 'true'); // it doesn't do boolean...
    // we try and we know. we don't try and we never know.

    // Function to apply caching lookup for images
    function applyImageCaching(img) {
        if (localStorage.getItem("mai-speed-server-status") == 'true') {
            // Get the image source URL
            const imgUrl = img.getAttribute('src');

            // Set the original path as a data attribute
            img.setAttribute('data-original-src', imgUrl);

            // Generate the cachePhoto URL with the image path
            //const cacheUrl = `http://127.0.0.1:8000/cachePhoto?path=${encodeURIComponent(imgUrl)}`;

            ///const cacheUrl = imgUrl.replace("://", "://mai-speed.evnchn.io/");

            const cacheUrl = imgUrl.replaceAll("\:\/\/", "://mai-speed.evnchn.io/");

            // Set the cachePhoto URL as the new source for the image
            img.setAttribute('src', cacheUrl);

            // Set the data attribute to indicate that caching has been applied to this image
            img.setAttribute('data-caching-applied', 'true');

            // Add an error event listener to the image
            img.addEventListener('error', function () {
                // Rollback the path using the data attribute
                const originalSrc = img.getAttribute('data-original-src');
                img.setAttribute('src', originalSrc);

                // Set the server status to false
                localStorage.setItem("mai-speed-server-status", 'false');
            });
        } else {
            console.log("Server not yet ready...");
        }
    }

    // Function to check if caching has been applied to the image
    function hasImageCachingApplied(img) {
        return img.getAttribute('data-caching-applied') === 'true';
    }

    // Function to apply caching to all images in the document
    function applyCachingToAllImages() {
        // Get all img tags in the document
        const imgTags = document.getElementsByTagName('img');

        // Iterate over each img tag
        for (let i = 0; i < imgTags.length; i++) {
            const img = imgTags[i];

            // Check if caching has already been applied to this image
            if (!hasImageCachingApplied(img)) {
                applyImageCaching(img);
            }
        }
    }

    applyCachingToAllImages();

    // Observer to detect DOM changes
    const observer = new MutationObserver(function (mutationsList) {
        for (const mutation of mutationsList) {
            if (mutation.type === 'childList') {
                const addedNodes = mutation.addedNodes;
                for (const node of addedNodes) {
                    if (node.nodeType === Node.ELEMENT_NODE && node.tagName === 'IMG') {
                        const img = node;
                        if (!hasImageCachingApplied(img)) {
                            // Check if server is up before applying caching to new images
                            applyCachingToAllImages();
                        }
                    }
                }
            }
        }
    });

    // Start observing changes in the DOM
    observer.observe(document.body, { childList: true, subtree: true });
})();