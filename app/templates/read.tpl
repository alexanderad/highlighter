% rebase('base.tpl', title=title, page_script='read.js')

<div class="container">
    <div class="row translatable">
        <div class="col s12">
            <h5>{{ title }}</h5>
        </div>
    </div>
    <div class="row">
        <div class="col s6">
            <i class="tiny material-icons">launch</i><span class="tiny-font tiny-icon-align">&nbsp;<a href="{{ url }}">{{ domain }}</a></span>
        </div>
        <div class="col s6 right-align">
            <i class="tiny material-icons">translate</i><span class="tiny-font tiny-icon-align">&nbsp;{{ lang }} &rightarrow; en</span>
        </div>
    </div>
    <div class="translatable">
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

