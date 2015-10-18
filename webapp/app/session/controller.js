import Ember from 'ember';

export default Ember.Controller.extend({

    needs_investigation: function() {
        return this.get('model.investigated') !== true && this.get('model.status') !== 'SUCCESS';
    }.property('model.investigated', 'model.status'),

    toggle: function(attr) {
        var self = this;
        self.api.call('toggle_' + attr, {session_id: parseInt(self.get('model.id'))}).then(function() {
            self.set('model.' + attr, !self.get('model.' + attr));
        }).then(function() {
            self.get('model').reload();
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
