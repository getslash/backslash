import Ember from 'ember';

export default Ember.Controller.extend({

    needs: ["application"],

    currentPath: function() {

        return this.controllerFor('application').get('currentPath');
    }.property()
});
