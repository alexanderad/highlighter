function getAPIHost() {
  return new Promise(resolve => {
    chrome.management.getSelf(info => {
      if (info.installType == "development") {
        resolve("http://localhost:8000");
      } else {
        resolve("https://highlighter.alpaca.engineering");
      }
    });
  });
}

function openHighlighterTab(url, set_active) {
  getAPIHost().then(apiHost => {
    chrome.tabs.create({
      url: apiHost + "/parse?u=" + encodeURI(url),
      active: set_active
    });
  });
}

chrome.browserAction.onClicked.addListener(function(tab) {
  openHighlighterTab(tab.url, true);
});
