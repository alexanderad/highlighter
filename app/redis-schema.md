# Known Redis Keys (read: _database schema_)

## Text Tree
* `text:<md5(text)>:<lang>` -- `text` in `lang`

## Page Tree
* `pages:<md5(url)>:page_id` -- `url` to `page_id` mapping
* `pages:<page_id>` -- source url for `page_id`
* `pages:<page_id>:title` -- `title` of page with `page_id`
* `pages:<page_id>:content` -- `content` of page with `page_id`
* `pages:<page_id>:image` -- lead `image` of page with `page_id`
* `pages:<page_id>:domain` -- `domain` of page with `page_id`
* `pages:<page_id>:next_page_url` -- `next_page_url` of page with `page_id` (if any)
* `pages:<page_id>:views` -- number of views for page with `page_id`

## Scoreboards
* `pages:recent` -- list of recent pages added

## Counters Tree
* `counters:requests:<view>` -- number of requests served by `view`
* `counters:characters:translated` -- number of translate characters (to track API limits)
