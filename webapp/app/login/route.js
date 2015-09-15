import Ember from 'ember';
import UnauthenticatedRouteMixin from 'ember-simple-auth/mixins/unauthenticated-route-mixin';

export default Ember.Route.extend(UnauthenticatedRouteMixin, {

    actions: {

        googleLogin: function() {
            let self = this;

            self.get('torii').open('google-oauth2').then(function(auth) {
                return self.get('session').authenticate('authenticator:token', auth).then(
                    function(data) {return data;},
                    function(error) {
                        self.controllerFor('application').send('login_error', error);
                    });
            });

            return;
        }
    }
});
