const cacheSize = 10;

function pronounce(text) {
  const u = new SpeechSynthesisUtterance();
  u.text = text;
  u.rate = 1;
  u.lang = "nl-NL";
  
  const voices = speechSynthesis.getVoices();
  const dutchVoices = voices.filter(voice => voice.lang.startsWith('nl'));
  
  if (dutchVoices.length > 0) {
    const randomVoice = dutchVoices[Math.floor(Math.random() * dutchVoices.length)];
    u.voice = randomVoice;
  }
  
  speechSynthesis.speak(u);
}

function drawWord(data) {
  document.getElementById("id-translation").innerText = data["translation"];
  let wordRepr = data["word"];
  if (data["pos"].includes("noun")) {
    wordRepr = `${data["noun_article"]} ${data["word"]}`.trim();
  }
  document.getElementById("id-word").innerText = wordRepr;
  document.getElementById("id-word").addEventListener("click", () => pronounce(data["word"]));
  document.getElementById("id-example").innerHTML = data["example"].replace(
    data["word"],
    `<span class="highlight">${data["word"]}</span>`
  );
  document.getElementById("id-example").addEventListener(
    "click",
    () => pronounce(data["example"]),
    false
  );

  document.getElementById(
    "id-meta"
  ).innerHTML = `${data["pos"]} &ndash; ${data["freq"]} in 100 documents`;
  console.log(`Word "${data["word"]}" seen times: ${data["seen_times"]}`);
}

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

async function getInstallationID() {
  const result = await chrome.storage.sync.get(["installationID"]);
  if (result.installationID) {
    return result.installationID;
  }
  
  const installationID = Math.random().toString(16);
  await chrome.storage.sync.set({ installationID });
  return installationID;
}

async function apiCall(url, method) {
  const installationID = await getInstallationID();
  const apiHost = await getAPIHost();
  
  const response = await fetch(apiHost + url, {
    method,
    headers: {
      "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
      "X-Installation-ID": installationID
    }
  });
  
  return response.json();
}

async function fetchWord() {
  const response = await apiCall("/v1/words/random", "POST");
  return response.data;
}

async function cacheWords() {
  const promised = Array(cacheSize).fill().map(() => fetchWord());
  const downloadedWords = await Promise.all(promised);
  
  const storage = await chrome.storage.sync.get({ words: [] });
  await chrome.storage.sync.set({ words: storage.words.concat(downloadedWords) });
}

async function getWord() {
  const result = await chrome.storage.sync.get({ words: [] });
  
  if (result.words.length > 0) {
    const word = result.words.pop();
    await chrome.storage.sync.set({ words: result.words });
    
    if (result.words.length < cacheSize / 2) {
      cacheWords();
    }
    return word;
  }
  
  await cacheWords();
  return fetchWord();
}

getWord().then(word => drawWord(word));
