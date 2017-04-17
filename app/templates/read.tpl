% rebase('base.tpl', title=title, page_script='read.js')

<div class="container">
    <a href="{{ url }}">{{ title }}</a><br />
    <i class="tiny material-icons">web</i><span class="tiny-icon-align">&nbsp;{{ domain }}</span>
    <div id="id-translatable">
        {{! content }}
    </div>
</div>

