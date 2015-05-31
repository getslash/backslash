import Ember from 'ember';

export default Ember.Route.extend({

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
