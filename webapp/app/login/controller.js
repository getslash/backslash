import Ember from 'ember';
import UnauthenticatedRouteMixin from 'ember-simple-auth/mixins/unauthenticated-route-mixin';

export default Ember.Controller.extend(UnauthenticatedRouteMixin, {
    authenticator: 'authenticator:torii',

    session: Ember.inject.service(),

    loading: false,

    actions: {

        googleLogin: function() {
            let self = this;
            self.set('loading', true);
            self.get('torii').open('google-oauth2').then(function(auth) {
                return self.get('session').authenticate('authenticator:token', auth).then(
                    function(data) {return data;},
                    function(error) {
                        self.controllerFor('application').send('login_error', error);
                    });
            }).finally(function() {
                self.set('loading', false);
            });

            return;
        }
    }

});
