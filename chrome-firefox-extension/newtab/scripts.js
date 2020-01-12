const cacheSize = 10;

function pronounce(text) {
  var u = new SpeechSynthesisUtterance();
  u.text = text;
  u.rate = 0.75;
  u.lang = "nl-NL";
  speechSynthesis.speak(u);
}

function drawWord(data) {
  document.getElementById("id-translation").innerText = data["translation"];
  var wordRepr = data["word"];
  if (data["pos"].includes("noun")) {
    wordRepr = `${data["noun_article"]} ${data["word"]}`.trim();
  }
  document.getElementById("id-word").innerText = wordRepr;
  document.getElementById("id-word").addEventListener("click", function(el) {
    pronounce(data["word"]);
  });
  document.getElementById("id-example").innerHTML = data["example"].replace(
    data["word"],
    `<span class="highlight">${data["word"]}</span>`
  );
  document.getElementById("id-example").addEventListener(
    "click",
    function(el) {
      pronounce(data["example"]);
    },
    false
  );

  document.getElementById(
    "id-meta"
  ).innerHTML = `${data["pos"]} &ndash; ${data["freq"]} in 100 documents`;
  console.log(`Word "${data["word"]}" seen times: ${data["seen_times"]}`);
}

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

function getInstallationID() {
  return new Promise(resolve => {
    chrome.storage.sync.get(["installationID"], result => {
      if (result.installationID) {
        resolve(result.installationID);
      } else {
        var installationID = Math.random().toString(16);
        chrome.storage.sync.set({ installationID: installationID });
        resolve(installationID);
      }
    });
  });
}

function apiCall(url, method) {
  return new Promise(resolve => {
    getInstallationID().then(installationID => {
      getAPIHost().then(apiHost => {
        fetch(apiHost + url, {
          method: method,
          headers: {
            "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Installation-ID": installationID
          }
        }).then(response => {
          response.json().then(data => resolve(data));
        });
      });
    });
  });
}

function fetchWord() {
  return new Promise(resolve => {
    apiCall("/v1/words/random", "POST").then(response =>
      resolve(response.data)
    );
  });
}

function cacheWords() {
  var promised = [];
  for (let i = 0; i < cacheSize; i++) {
    promised.push(fetchWord());
  }
  Promise.all(promised).then(downloadedWords => {
    chrome.storage.sync.get({ words: [] }, storage => {
      chrome.storage.sync.set({ words: storage.words.concat(downloadedWords) });
    });
  });
}

function getWord() {
  return new Promise(resolve => {
    chrome.storage.sync.get({ words: [] }, result => {
      if (result.words.length > 0) {
        word = result.words.pop();
        chrome.storage.sync.set({ words: result.words });
        if (result.words.length < cacheSize / 2) {
          cacheWords();
        }
        resolve(word);
      } else {
        cacheWords();
        fetchWord().then(word => resolve(word));
      }
    });
  });
}

getWord().then(word => drawWord(word));
