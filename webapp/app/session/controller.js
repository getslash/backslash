import Ember from 'ember';

export default Ember.Controller.extend({

    needs: ["application"],

    currentPath: function() {

        return this.controllerFor('application').get('currentPath');
    }.property(),

    toggle: function(attr) {
        var self = this;
        self.api.call('toggle_' + attr, {session_id: parseInt(self.get('model.id'))}).then(function() {
            self.set('model.' + attr, !self.get('model.' + attr));
        }).then(function() {
            self.send('refreshRoute');
        });
    },

    actions: {

        toggle_archive: function() {
            this.toggle('archived');
        },

        toggle_investigated: function() {
            this.toggle('investigated');
        }
    }
});
