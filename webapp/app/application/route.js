import Ember from 'ember';
import ApplicationRouteMixin from 'simple-auth/mixins/application-route-mixin';

export default Ember.Route.extend(ApplicationRouteMixin, {


    actions: {
        gotoSession: function (session) {
            this.transitionTo('session', session);
        },
        gotoTest: function(test) {
            this.transitionTo('test', test);
        }
    }
});
