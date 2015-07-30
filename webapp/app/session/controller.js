import Ember from 'ember';

export default Ember.Controller.extend({

    needs: ["application"],

    currentPath: function() {

        return this.controllerFor('application').get('currentPath');
    }.property(),

    actions: {

        toggle_archive: function() {
            var self = this;
            self.api.call('toggle_archived', {session_id: parseInt(self.get('model.id'))}).then(function() {
                self.set('model.archived', !self.get('model.archived'));
            });
        }
    }
});
