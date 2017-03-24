$(function () {

    $('#id-translatable').on('mouseup', function () {
        processSelection();
    });

    $(document).on('text:translated', function (event, text, translated, selectionId) {
        var tooltip = $('<span class="tooltiptext"></span>').text(translated || text);
        $('#' + selectionId).append(tooltip);

        var tooltipClientWidth = tooltip.get(0).clientWidth;
        tooltip.css('width', tooltipClientWidth + 10);
        tooltip.css('margin-left', -(tooltipClientWidth + 10) / 2);
    });

    $(document).on('text:selected', function (event, text, selection, range) {
        var selectionId = getRandomId();
        var tooltip = $(
            '<span class="tooltip highlight-underline"></span>'
        ).attr('id', selectionId).get(0);
        $(tooltip).on('click', function (event) {
            $(document).trigger('tooltip:clicked', [event]);
        });

        range.surroundContents(tooltip);
        $(document).trigger('text:wrapped', [text, selectionId]);
    });

    $(document).on('text:wrapped', function (event, text, selectionId) {
        $.post('/v1/translate', {'text': text}, function (response) {
            if (response.success) {
                $(document).trigger('text:translated', [text, response.text, selectionId]);
            } else {
                console.log(response);
            }
        });
    });

    $(document).on('tooltip:clicked', function(event, click_event) {
        var tooltip = $(click_event.currentTarget);
        tooltip.children().remove();
        tooltip.replaceWith(tooltip.text());
    });

    function getRandomId() {
        return 'id-translate-' + Math.floor(new Date());
    }

    function processSelection() {
        var selection = window.getSelection();
        if (selection.isCollapsed) return;
        var range = selection.getRangeAt(0).cloneRange();
        var text = selection.toString().trim();
        if (text.length > 0 && text.length < 128) {
            $(document).trigger('text:selected', [text, selection, range]);
        } else {
            console.log('selected text is too long or empty')
        }
        window.getSelection().empty();

    }

});
