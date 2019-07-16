(function() {
  function fetchWord() {
    fetch("http://highlighter.alpaca.engineering/v1/words/random")
      .then(response => response.json())
      .then(json => {
        drawWord(json["data"]);
      });
  }

  function drawWord(data) {
    console.log(data);
    ["word", "pos", "freq", "translation"].forEach(element => {
      document.getElementById("id-" + element).innerText = data[element];
    });

    document.getElementById("id-example").innerHTML =
      '"' +
      data["example"].replace(
        new RegExp(data["word"], "g"),
        "<b>" + data["word"] + "</b>"
      ) +
      '"';
  }

  fetchWord();
})();
