import Ember from 'ember';

export default Ember.Controller.extend({
    conclusion: '',

    actions: {
        submit: function() {
            var self = this;
            const sid = parseInt(self.get('model.id'));
            self.api.call('post_comment', {
                comment: self.get('conclusion'),
                session_id: sid
            }).then(function() {
                self.api.call('toggle_investigated', {
                    session_id: sid
                });
            }).then(function() {
                self.get('model').reload();
                window.history.back();
            });
        },
    }
});
