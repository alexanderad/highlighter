function getRootNamespace() {
  var isChrome = !!window.chrome;
  var isFirefox = typeof InstallTrigger !== "undefined";

  if (isChrome) {
    return chrome;
  }
  if (isFirefox) {
    return browser;
  }
}

var installationID;
var rootNamespace = getRootNamespace();

function openHighlighterTab(url, set_active) {
  rootNamespace.tabs.create({
    url: "https://highlighter.alpaca.engineering/parse?u=" + encodeURI(url),
    active: set_active
  });
}

rootNamespace.browserAction.onClicked.addListener(function(tab) {
  openHighlighterTab(tab.url, true);
});

rootNamespace.storage.sync.get("installationID", function(items) {
  installationID = items.installationID;
  if (!items.installationID) {
    installationID = Math.random()
      .toString(16)
      .substr(2, 10);
    chrome.storage.sync.set({ installationID: installationID });
  }
});
