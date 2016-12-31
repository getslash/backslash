import Ember from 'ember';

const _DEFAULTS = {
    humanize_times: true,
    comments_expanded: false,
    show_side_labels: false,
};

let _classvars = {};

let _setting = Ember.computed({
    set(key, value) {
        localStorage.setItem('display.' + key, value === true);
        this.set('_cache_' + key, value);
        return value;
    },

    get(key) {
        console.log('getting', key);
        let value = this.get('_cache_' + key);

        if (value !== undefined) {
            return value;
        }

        value = localStorage.getItem('display.' + key);
        if (value !== 'true' && value !== 'false') {
            return _DEFAULTS[key];
        }
        return value === "true";
    }
});

for (let field_name in _DEFAULTS) {
    if (_DEFAULTS.hasOwnProperty(field_name)) {
        _classvars[field_name] = _setting;
    }
}

export default Ember.Service.extend(_classvars);
