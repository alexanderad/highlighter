chrome.browserAction.onClicked.addListener(function(tab) {
    chrome.tabs.create({
        "url": "https://highlighter.darednaxella.name/parse?u=" + encodeURI(tab.url)
    });
});
