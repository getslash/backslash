import Ember from 'ember';

export default Ember.Component.extend({
    frame: null,
    show_vars: false,

    has_locals: Ember.computed.notEmpty('frame.locals'),
    has_globals: Ember.computed.notEmpty('frame.globals'),

    actions: {
        toggle: function() {
            this.set('show_vars', !this.get('show_vars'));
        }
    }
});
