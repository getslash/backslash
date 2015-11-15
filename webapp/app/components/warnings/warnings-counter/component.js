import Ember from 'ember';

export default Ember.Component.extend({
    classNames: ['warnings-counter'],
    classNameBindings: ['has_warnings:warning'],

    has_warnings: function() {
        return this.get('obj.num_warnings') > 0;
    }.property('obj.num_warnings')
});
