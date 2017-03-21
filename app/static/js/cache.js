// simple filo-style cache :-)
var Cache = function (maxSize) {
    this._keys = [];
    this._items = {};
    this._size = 0;
    this._maxSize = maxSize || 1024;
};

Cache.prototype = {
    set: function (key, value) {
        if (this._items.hasOwnProperty(key)) return;

        this._keys[this._size] = key;
        this._items[key] = value;
        this._size = this._keys.length;

        if (this._size > this._maxSize) {
            removed_key = this._keys.shift();
            delete this._items[removed_key];
            this._size = this._keys.length;
        }
    },

    get: function (key) {
        if (this._items.hasOwnProperty(key)) {
            return this._items[key];
        }
    },

    hasKey: function (key) {
        return this._items.hasOwnProperty(key);
    }
}
