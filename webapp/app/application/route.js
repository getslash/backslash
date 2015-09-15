import Ember from 'ember';
import ApplicationRouteMixin from 'ember-simple-auth/mixins/application-route-mixin';

export default Ember.Route.extend(ApplicationRouteMixin, {


    actions: {
        goto_session: function (session) {
            this.transitionTo('session', session);
        },
        goto_test: function(test) {
            this.transitionTo('test', test);
        }
    }
});
