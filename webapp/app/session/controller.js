import Ember from 'ember';

export default Ember.Controller.extend({

    currentPath: function() {

        return this.controllerFor('application').get('currentPath');
    }.property()
});
