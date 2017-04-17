% rebase('base.tpl', title=None, page_script=None)

<div class="row valign-wrapper block-80vh">
    <div class="col s2"></div>

    <div class="col s8">
        <form action="/parse" method="GET">
            <div class="input-field">
              <input id="id-article-url" name="u" type="text" autocomplete="false">
              <label for="id-article-url">Article URL</label>
            </div>
        </form>
    </div>

    <div class="col s2"></div>
</div>
