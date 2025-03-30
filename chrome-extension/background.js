async function getAPIHost() {
  const devHost = "http://localhost:8000";
  const prodHost = "https://highlighter.darednaxella.name";
  
  try {
    const info = await chrome.management.getSelf();
    if (info.installType === "development") {
      try {
        await fetch(devHost + "?ping");
        return devHost;
      } catch {
        return prodHost;
      }
    }
    return prodHost;
  } catch (error) {
    console.error('Error getting API host:', error);
    return prodHost;
  }
}

async function openHighlighterTab(url, set_active) {
  try {
    const apiHost = await getAPIHost();
    await chrome.tabs.create({
      url: `${apiHost}/parse?u=${encodeURI(url)}`,
      active: set_active
    });
  } catch (error) {
    console.error('Error opening Highlighter tab:', error);
  }
}

// Listen for clicks on the extension icon
chrome.action.onClicked.addListener((tab) => {
  openHighlighterTab(tab.url, true);
});
