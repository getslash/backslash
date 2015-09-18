import Ember from 'ember';

export default Ember.Component.extend({
    to: null,
    tagName: 'li',
    current_path: null,

    classNameBindings: ['is_active:active'],

    is_active: function() {
        return this.get('current_path') === this.get('to');
    }.property('to', 'current_path')

});
