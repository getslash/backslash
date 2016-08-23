import Ember from 'ember';
import UnauthenticatedRouteMixin from 'ember-simple-auth/mixins/unauthenticated-route-mixin';

export default Ember.Controller.extend(UnauthenticatedRouteMixin, {
    authenticator: 'authenticator:torii',

    session: Ember.inject.service(),

    loading: false,

    actions: {

	login() {
	    let self = this;
	    self.set('login_error', null);
	    const credentials = this.getProperties(['username', 'password']);
	    self.get('session').authenticate('authenticator:token', credentials).then(function() {
	    }, function() {
		self.set('login_error', 'Invalid username and/or password');
	    });
	},

        login_google() {
            let self = this;
            self.set('loading', true);
	    self.set('login_error', null);
            self.get('torii').open('google-oauth2').then(function(auth) {
                return self.get('session').authenticate('authenticator:token', auth).then(
                    function(data) {return data;},
                    function(error) {
                        self.set('login_error', error.error);
                    });
            }).finally(function() {
                self.set('loading', false);
            });

            return;
        }
    }

});
