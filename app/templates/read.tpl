% rebase('base.tpl', title=title, page_script='read.js')

<div class="container">
    <div class="row">
        <div class="col s12">
            <a href="{{ url }}">{{ title }}</a>
        </div>
    </div>
    <div class="row">
        <div class="col s6">
            <i class="tiny material-icons">label</i><span class="tiny-font tiny-icon-align">&nbsp;{{ domain }}</span>
        </div>
        <div class="col s6 right-align">
            <i class="tiny material-icons">translate</i><span class="tiny-font tiny-icon-align">&nbsp;{{ lang }} &rightarrow; en</span>
        </div>
    </div>
    <div id="id-translatable">
        {{! content }}
    </div>
    <div class="row tiny-font">
        <div class="col s6">
            Highlighter
        </div>
        <div class="col s6 right-align">
            <a href="http://translate.yandex.com/">translations powered by Yandex.Translate</a>
        </div>
    </div>
</div>

