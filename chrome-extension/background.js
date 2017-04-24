chrome.browserAction.onClicked.addListener(function(tab) {
    chrome.tabs.create({
        "url": "https://highlighter.darednaxella.name/parse?source=chrome-extension&u=" + encodeURI(tab.url)
    });
});
