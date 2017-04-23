% rebase('base.tpl', title=title, page_script='read.js')

<div class="container">
    <div class="row translatable">
        <div class="col s12">
            <h5>{{ title }}</h5>
        </div>
    </div>
    <div class="row">
        <div class="col s6">
            <a class="btn-flat btn-sm" href="{{ url }}"><i class="material-icons icons-sm">launch</i> {{ domain }}</a>
        </div>
        <div class="col s6 right-align">
          <a class="dropdown-button btn-flat btn-sm" data-beloworigin="true" href="#" data-activates="dropdown-langs">
              <i class="material-icons icons-sm">translate</i> {{ lang }} &rightarrow; {{ dest_lang }}
          </a>

          <ul id="dropdown-langs" class="dropdown-content">
            % for code, lang in dest_langs.items():
                <li><a href="/read?t={{ page_id }}&l={{ code }}">{{ lang }}</a></li>
            % end
          </ul>

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

