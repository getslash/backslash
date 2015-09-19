import Ember from 'ember';
import PathObserver from '../mixins/path-observer';


export default Ember.Controller.extend(PathObserver, {

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
