import Ember from 'ember';

export default Ember.Controller.extend({
    api: Ember.inject.service(),
    conclusion: '',

    actions: {
        submit: function() {
            var self = this;
            const sid = parseInt(self.get('model.id'));
            self.get('api').call('post_comment', {
                comment: self.get('conclusion'),
                session_id: sid
            }).then(function() {
                self.get('api').call('toggle_investigated', {
                    session_id: sid
                });
            }).then(function() {
                self.get('model').reload();
                window.history.back();
            });
        },
    }
});
