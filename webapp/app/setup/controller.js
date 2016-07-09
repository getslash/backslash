import Ember from 'ember';

export default Ember.Controller.extend({

    api: Ember.inject.service(),
    admin_user_password_2: "",
    admin_user_password: Ember.computed.alias('config.admin_user_password'),

    passwords_match: function() {
	return this.get('admin_user_password') && this.get('admin_user_password') === this.get('admin_user_password_2');
    }.property('admin_user_password', 'admin_user_password_2'),

    passwords_mismatch: function() {
	return (this.get('admin_user_password') || this.get('admin_user_password_2')) && this.get('admin_user_password') !== this.get('admin_user_password_2');
    }.property('admin_user_password', 'admin_user_password_2'),

    password_classes: function() {
	if (this.get('passwords_mismatch')) {
	    return 'has-error';
	} else if (this.get('passwords_match')) {
	    return 'has-success';
	}
	return '';
    }.property('passwords_match', 'password_mismatch'),

    actions: {
	setup() {
	    let self = this;
	    self.get('api').call('setup', {
		config: this.get('config'),
		}).then(function() {
		    window.location.href="/";
		});

	},
    },
});
