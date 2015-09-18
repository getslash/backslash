import Ember from 'ember';

export default Ember.Controller.extend({

    user: Ember.computed.oneWay('model.user'),
    tokens: Ember.computed.oneWay('model.tokens'),

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
            self.api.call('toggle_user_role', {
                user_id: parseInt(this.get('model.id')),
                role: role}).then(function() {
                    self.send('refreshRoute');
                });
        }
    }
});
