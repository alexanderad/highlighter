% rebase('base.tpl', title=None, page_script=None)

<div class="row valign-wrapper almost-full-page">
    <div class="col s2"></div>
    <div class="col s8">
        <div class="row center-align">
            <h3>High
                <span class="highlight">light</span>er</h3>
        </div>
        <div class="row">
            <form action="/parse" method="GET">
                <nav class="white">
                    <div class="nav-wrapper">
                        <form>
                            <div class="input-field">
                                <input id="id-article-url" name="u" type="search" autocomplete="false" placeholder="paste page or article address">
                                <label class="label-icon" for="id-article-url">
                                    <i class="material-icons">link</i>
                                </label>
                            </div>
                        </form>
                    </div>
                </nav>
            </form>
        </div>
    </div>
    <div class="col s2"></div>
</div>
<div class="row">
    <div id="id-add-extension" class="col s12 center-align hidden">
        <a id="id-add-extension-a" class="btn btn-flat btn-sm waves-effect waves-light" href="#">
            <i class="material-icons icons-sm">extension</i>
        </a>
    </div>
</div>
<script>
    function createExtensionLink() {
        var isChrome = !!window.chrome;
        var isFirefox = typeof InstallTrigger !== 'undefined';

        if (isChrome) {
            $('#id-add-extension-a').attr('href', 'https://chrome.google.com/webstore/detail/highlighter/jgpefkfmeadeefefhnehncpbnaopfkbc');
            $('#id-add-extension-a').append('add to chrome');
        }

        if (isFirefox) {
            $('#id-add-extension-a').attr('href', '/static/etc/highlighter-1.3.2.xpi');
            $('#id-add-extension-a').append('add to firefox');
        }

        if (isFirefox || isChrome) $('#id-add-extension').fadeIn();
    }

    $(function () {
        $('#id-article-url').focus();
        createExtensionLink();
    })
</script>
