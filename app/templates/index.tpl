<html>
  <head>
    <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,300i" rel="stylesheet">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
    <style type="text/css">
      html {
        font-family: 'Open Sans', sans-serif;
        font-size: 24px;
        line-height: 2.2;
      }

      ::selection {
        background: #FFD84D;
      }
      ::-moz-selection {
        background: #FFD84D;
      }

      .container {
        text-align: justify;
        width:900px;
        margin: 100 auto;
      }

      .tooltip {
          position: relative;
          display: inline-block;
      }

      .highlight-underline {
        position: relative;
      }
      .highlight-underline::after{
          content:'';
          position:absolute;
          width: 100%;
          height: 0;
          left: 0;
          bottom: 2px;
          border-bottom: 4px solid #FFD84D;
      }

      .tooltip .tooltiptext {
          /*visibility: hidden;*/
          opacity: 1;
          /*width: 120px;*/
          background-color: #FFD84D;
          color: black;
          line-height: 1.0;
          font-size: 60%;
          font-weight: bold;
          text-align: center;
          border-radius: 6px;
          padding: 2px 0;
          position: absolute;
          z-index: 1;
          bottom: 80%;
          left: 50%;
          /*margin-left: -60px;*/
          white-space: nowrap;
      }

      .tooltip .tooltiptext::after {
          content: "";
          position: absolute;
          top: 100%;
          left: 50%;
          margin-left: -5px;
          border-width: 5px;
          border-style: solid;
          border-color: #FFD84D transparent transparent transparent;
      }

      /*.tooltip:hover .tooltiptext {
          visibility: visible;
      }*/

    </style>
    <script type="text/javascript">

      // simple filo-style cache :-)
      var Cache = function (maxSize) {
        this._keys = [];
        this._items = {};
        this._size = 0;
        this._maxSize = maxSize || 1024;
      };

      Cache.prototype = {
        set: function(key, value) {
          if (this._items.hasOwnProperty(key)) return;

          this._keys[this._size] = key;
          this._items[key] = value;
          this._size = this._keys.length;

          if (this._size > this._maxSize) {
            removed_key = this._keys.shift();
            delete this._items[removed_key];
            this._size = this._keys.length;
          }
        },

        get: function(key) {
          if (this._items.hasOwnProperty(key)) {
            return this._items[key];
          }
        },

        hasKey: function(key) {
          return this._items.hasOwnProperty(key);
        }
      }

      $(function() {

        var cache = new Cache(64);

        $('#id-translatable').on('mouseup', function() {
            processSelection();
        });

        $(document).on('text:translated', function(event, text, translated, selectionId) {
          var tooltip = $('<span class="tooltiptext"></span>').text(translated || text);
          $('#' + selectionId).append(tooltip);

          var tooltipClientWidth = tooltip.get(0).clientWidth;
          console.log(tooltipClientWidth);
          tooltip.css('width', tooltipClientWidth + 10);
          tooltip.css('margin-left', -tooltipClientWidth / 2);
        });

        $(document).on('text:selected', function(event, text, selection, range) {
          var selectionId = getRandomId();
          var tooltip = $(
            '<span class="tooltip highlight-underline"></span>'
          ).attr('id', selectionId).get(0);
          range.surroundContents(tooltip);
          $(document).trigger('text:wrapped', [text, selectionId]);
        })

        $(document).on('text:wrapped', function(event, text, selectionId) {
          if (cache.hasKey(text)) {
            translated = cache.get(text);
            $(document).trigger('text:translated', [text, translated, selectionId]);
          }
          else {
            $.getJSON('/translate?text=' + text, function(response) {
              if (response.success) {
                translated = response.text;
                cache.set(text, translated);
                $(document).trigger('text:translated', [text, translated, selectionId]);
              } else {
                console.log(response);
              }
            });
          }
        });

        function getRandomId() {
          return 'id-translate-' + Math.floor(new Date());
        };

        function processSelection() {
            if (window.getSelection) {
                selection = window.getSelection();
                range = selection.getRangeAt(0).cloneRange();
                text = selection.toString();
                if (text.length > 0 && text.length < 128) {
                    $(document).trigger('text:selected', [text, selection, range]);
                } else {
                  console.log('selected text is too long or empty')
                }
                window.getSelection().empty();
            };
        };

      });


    </script>
  </head>

      <body>
          <div id="id-translatable" class="container">
De aproape cincizeci de ani, din turnul şcolii
supraveghea cu cadranele sale cele patru puncte cardinale; de aproape
cincizeci de ani, acele sale enorme indicau fără greşeală ora exactă.
Rareori, iarna, în timpul viscolelor, zăpada cotropitoare oprea mersul lor
pe cadranul dinspre soare răsare, iar primăvara, hulubii sau ciorile sau
alte zburătoare, în zbenguiala lor, grăbeau mersul vreunui minutar. Dar
de fiecare dată, moş Timofte Păstrăvanu, paznicul şcolii, care-şi începuse
meseria aceasta încă de pe vremea instalării marelui ornic, şi care, aşa
cum spuneau elevii din clasele superioare, şi-o va încheia doar o dată cu
oprirea definitivă a ceasului, se urca în turn, scutura scripeţii uriaşi şi
începea să învârtească o manivelă cât oiştea carului. După ce asculta
câteva clipe tic-tacul tunător şi clătina din cap a încuviinţare, moş
Timofte scotea de la brâu o cutie rotundă de metal, cândva strălucitoare,
o cutie mare cât o farfurie, o proptea pe genunchi şi o pocnea cu pumnul
în creştet. Ca la comandă, cutia lepăda un capac pentru a dezveli un
cadran de ceas cu aceleaşi cifre romane care împodobeau
feţele orologiului din turn. Paznicul scruta cu atenţie ora exactă şi
potrivea întocmai acele "Gîngălăului", pentru că aşa numea dânsul
ceasul din turn. O dată treaba terminată, închidea cu câteva zdravene
lovituri de pumn capacul "Ţîngălăului", pentru că aşa numea dânsul
ceasul de la brâu. E de prisos să amintim că lanţul care purta dihania
aceea de metal ar fi putut struni un cogeamite dulău ciobănesc. Apoi, în
mers agale, bătrânul cobora scările, ieşea în curte, se oprea în mijlocul
ei, citea cu voce tare ora exactă de pe ceasul din turn şi, dacă era în
timpul lecţiilor, făcea iute o socoteală, tot cu voce tare, cam cât mai
rămâne până la recreaţie. Şi chiar dacă mai rămâneau patruzeci de
minute până când trebuia să sune clopoţelul, moş Timofte nu mai
cerceta nici Gîngălăul, nici Ţîngălăul. Putea să fie împovărat de treburi,
putea să fie asaltat de griji, la secunda exactă, clopoţelul suna, în mâna
lui, sfârşitul orei.
          </div>
        </body>


</html>
