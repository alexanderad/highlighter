$(function () {
    var source_lang, dest_lang;

    // $('.translatable').on('mouseup', function () {
    //     processSelection();
    // });

    $('.translatable').on('mouseup', function() {
        rangy.getSelection().expand("word", {
            trim: true,
            wordOptions: {
                wordRegex: /[a-z0-9\u0218\u0219\u021A\u021B\u015E\u015F\u0162\u0163\u0102\u0103\u00C2\u00E2\u00CE\u00EE]+(['\-][a-z0-9\u0218\u0219\u021A\u021B\u015E\u015F\u0162\u0163\u0102\u0103\u00C2\u00E2\u00CE\u00EE]+)*/gi
            }
        });
        processSelection();
    });

    $(document).on('text:translated', function (event, text, translated, selectionId) {
        var tooltip = $('<span class="tooltiptext z-depth-1 valign-wrapper center-align"></span>').text(translated || text);
        $('#' + selectionId).append(tooltip);

        var tooltipClientWidth = tooltip.get(0).clientWidth;
        tooltip.css('width', tooltipClientWidth);
        tooltip.css('margin-left', -(tooltipClientWidth) / 2);
    });

    function rangeContainsTooltips(range) {
        return range.toHtml().search('tooltip') > 0;
    }

    $(document).on('text:selected', function (event, text, selection, range) {
        console.log(range.toHtml(), rangeContainsTooltips(range));

        var selectionId = getRandomId();
        var tooltip = $(
            '<span class="tooltip highlight-underline"></span>'
        ).attr('id', selectionId).get(0);

        // $(tooltip).on('click', function (event) {
        //     $(document).trigger('tooltip:clicked', [event]);
        // });

        if (range.canSurroundContents(tooltip)) {
            range.surroundContents(tooltip);
            $(document).trigger('text:wrapped', [text, selectionId]);
        }
        else {
            console.log('can not surround contents of selected range');
            selection.nativeSelection.empty();
        }
    });

    $(document).on('text:wrapped', function (event, text, selectionId) {
        $.post('/v1/translate', {'text': text, 'source_lang': source_lang, 'dest_lang': dest_lang}, function (response) {
            if (response.success) {
                $(document).trigger('text:translated', [text, response.text, selectionId]);
            } else {
                console.log(response);
            }
        });
    });

    $(document).on('text:announced_langs', function (event, announced_source_lang, announced_dest_lang) {
       source_lang = announced_source_lang;
       dest_lang = announced_dest_lang;
    });

    // $(document).on('tooltip:clicked', function(event, click_event) {
    //     var tooltip = $(click_event.currentTarget);
    //     tooltip.children().remove();
    //     tooltip.replaceWith(tooltip.text());
    // });

    function getRandomId() {
        return 'id-translate-' + Math.floor(new Date());
    }

    function processSelection() {
        var selection = rangy.getSelection();
        var range = selection.rangeCount ? selection.getRangeAt(0) : null;

        if (!range) {
            console.log('no range selected');
            return;
        }

        var text = selection.toString().trim();
        if (text.length > 0 && text.length < 128) {
            $(document).trigger('text:selected', [text, selection, range]);
        } else {
            console.log('selected text is too long or empty')
        }
    }
});
