import Ember from 'ember';

export default Ember.Controller.extend({

    roles: function() {
        let user_roles = [];
        this.get('model.user_roles').forEach(role => user_roles.push(role.name));
        let returned = [];

        ['admin', 'moderator', 'proxy'].forEach(function (name) {
            returned.push({name: name, enabled: user_roles.indexOf(name) !== -1});
        });
        return returned;
    }.property('model.user_roles.@each'),

    actions: {
        toggle: function(role) {
            let self = this;
            self.api.call('toggle_user_role', {
                user_id: parseInt(this.get('model.id')),
                role: role}).then(function() {
                    self.send('refreshRoute');
                });
        }
    }
});
