(function() {
  function fetchWord() {
    fetch("https://highlighter.alpaca.engineering/v1/words/random")
      .then(response => response.json())
      .then(json => {
        drawWord(json["data"]);
      });
  }

  function pronounce(text) {
    var u = new SpeechSynthesisUtterance();
    u.text = text;
    u.rate = 0.75;
    u.lang = "nl-NL";
    speechSynthesis.speak(u);
  }

  function drawWord(data) {
    ["word", "translation"].forEach(element => {
      document.getElementById("id-" + element).innerText = data[element];
    });
    document.getElementById("id-word").addEventListener("click", function(el) {
      pronounce(data["word"]);
    });
    document.getElementById("id-example").innerHTML = data["example"];
    document.getElementById("id-example").addEventListener(
      "click",
      function(el) {
        pronounce(data["example"]);
      },
      false
    );

    document.getElementById("id-meta").innerText = [
      data["pos"],
      data["freq"]
    ].join(", ");
  }

  fetchWord();
})();
