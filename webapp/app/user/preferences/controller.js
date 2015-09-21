import Ember from 'ember';

export default Ember.Controller.extend({

    user: Ember.computed.oneWay('model.user'),
    tokens: Ember.computed.oneWay('model.tokens'),
    session: Ember.inject.service(),

    roles: function() {
        let user_roles = [];
        this.get('user.user_roles').forEach(role => user_roles.push(role.name));
        let returned = [];

        ['admin', 'moderator', 'proxy'].forEach(function (name) {
            returned.push({name: name, enabled: user_roles.indexOf(name) !== -1});
        });
        return returned;
    }.property('model.user_roles'),

    actions: {
        toggle: function(role) {
            let self = this;
            if (role === 'admin' && self.get('user.email') === self.get('session.data.authenticated.user_info.email')) {
                if (!window.confirm('You are about to drop your own admin privileges. Are you sure?')) {
                    return;
                }
            }
            self.api.call('toggle_user_role', {
                user_id: parseInt(this.get('model.id')),
                role: role}).then(function() {
                    self.send('refreshRoute');
                });
        }
    }
});
