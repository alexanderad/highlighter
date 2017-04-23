% rebase('base.tpl', title=None, page_script=None)

<div class="row valign-wrapper almost-full-page">
    <div class="col s2"></div>

    <div class="col s8">
        <div class="row center-align">
            <h3>High<span class="highlight">light</span>er</h3>
        </div>
        <div class="row">
            <form action="/parse" method="GET">
                <nav class="white">
                    <div class="nav-wrapper">
                      <form>
                        <div class="input-field">
                          <input id="id-article-url" name="u" type="search" autocomplete="false">
                          <label class="label-icon" for="id-article-url"><i class="material-icons">launch</i></label>
                        </div>
                      </form>
                    </div>
                </nav>
            </form>
        </div>
    </div>

    <div class="col s2"></div>
</div>
<script>
    $(function () {
        $('#id-article-url').focus();
    })
</script>
