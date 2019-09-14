function openHighlighterTab(url, set_active) {
  chrome.tabs.create({
    url: apiHost + "/parse?u=" + encodeURI(url),
    active: set_active
  });
}

chrome.browserAction.onClicked.addListener(function(tab) {
  openHighlighterTab(tab.url, true);
});
