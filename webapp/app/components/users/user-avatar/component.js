import Ember from 'ember';

export default Ember.Component.extend({

    classNames: "user-avatar",
    classNameBindings: ['small'],

    email: null,
    user: null,
    _false: false,

    user_email: function() {
        if (this.get('user')) {
            return this.get('user.email');
        }
        return this.get('email');
    }.property('user', 'email'),


    is_admin: function() {
        return this._has_role('admin');
    }.property('user.user_roles'),

    is_moderator: function() {
        return this._has_role('moderator');
    }.property('user.user_roles'),

    _has_role: function(role) {
        let roles = [];
        this.get('user.user_roles').forEach(r => roles.push(r.name));
        return roles.indexOf(role) !== -1;
    }
});
