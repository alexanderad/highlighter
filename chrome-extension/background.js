const apiHost = "https://highlighter.darednaxella.name"

async function openHighlighterTab(url, set_active) {
  try {
    await chrome.tabs.create({
      url: `${apiHost}/parse?u=${encodeURI(url)}`,
      active: set_active,
    })
  } catch (error) {
    console.error("Error opening Highlighter tab:", error)
  }
}

// Listen for clicks on the extension icon
chrome.action.onClicked.addListener((tab) => {
  openHighlighterTab(tab.url, true)
})
