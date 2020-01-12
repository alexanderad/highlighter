function getAPIHost() {
  const devHost = "http://localhost:8000";
  const prodHost = "https://highlighter.darednaxella.name";
  return new Promise(resolve => {
    chrome.management.getSelf(info => {
      if (info.installType == "development") {
        fetch(devHost + "?ping")
          .then(() => {
            resolve(devHost);
          })
          .catch(() => {
            resolve(prodHost);
          });
      } else {
        resolve(prodHost);
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
