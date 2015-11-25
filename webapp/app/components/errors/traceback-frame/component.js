import Ember from 'ember';

export default Ember.Component.extend({
    frame: null,
    show_vars: false,

    has_locals: function() {
        return this._is_not_empty('frame.locals');
    }.property('frame'),

    has_globals: function() {
        return this._is_not_empty('frame.globals');
    }.property('frame'),

    _is_not_empty: function(attr) {
        const obj = this.get(attr);
        for (var key in obj) {
            if (obj.hasOwnProperty(key) && key[0] !== '_') {
                return true;
            }
        }
        return false;
    },

    actions: {
        toggle: function() {
            this.set('show_vars', !this.get('show_vars'));
        }
    }
});
