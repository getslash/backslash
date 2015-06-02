import Ember from 'ember';

export default Ember.Component.extend({
    tagName: 'li',
    classNameBindings: ['isActive:active'],

    route: null,

    isActive: function() {
        return this.get('linkto') === this.get('route');

    }.property('route')
});
