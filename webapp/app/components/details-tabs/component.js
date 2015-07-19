import Ember from 'ember';

export default Ember.Component.extend({

    obj: null,

    objtype: function() {
        return this.get('obj.constructor.modelName');
    }.property('obj'),

    index_route: function() {
        return this.get('objtype') + '.index';
    }.property('objtype'),


    errors_route: function() {
        return this.get('objtype') + '.errors';
    }.property('objtype'),

    comments_route: function() {
        return this.get('objtype') + '.comments';
    }.property('objtype'),

    errors_caption: function() {
        let num_errors = this.get('obj.num_errors');
        return 'Errors (' + num_errors + ')';
    }.property('obj')
});
