function openHighlighterTab(url, set_active) {
    chrome.tabs.create({
        "url": "https://highlighter.darednaxella.name/parse?u=" + encodeURI(url),
        "active": set_active
    });
}

chrome.contextMenus.create({
    "id": "id-open-link-in-highlighter",
    "title": "Send to Highlighter",
    "contexts": ["link"]
});

chrome.browserAction.onClicked.addListener(function(tab) {
    openHighlighterTab(tab.url, true);
});

chrome.contextMenus.onClicked.addListener(function(info, tab) {
    openHighlighterTab(info.linkUrl, false);
});
