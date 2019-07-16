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

var rootNamespace = getRootNamespace();

function openHighlighterTab(url, set_active) {
  rootNamespace.tabs.create({
    url: "https://highlighter.alpaca.engineering/parse?u=" + encodeURI(url),
    active: set_active
  });
}

rootNamespace.contextMenus.create({
  id: "id-open-link-in-highlighter",
  title: "Send to Highlighter",
  contexts: ["link"]
});

rootNamespace.browserAction.onClicked.addListener(function(tab) {
  openHighlighterTab(tab.url, true);
});

rootNamespace.contextMenus.onClicked.addListener(function(info, tab) {
  openHighlighterTab(info.linkUrl, false);
});
