import Ember from 'ember';
import ApplicationRouteMixin from 'ember-simple-auth/mixins/application-route-mixin';

export default Ember.Route.extend(ApplicationRouteMixin, {

    actions: {
        goto_session: function (session) {
            this.transitionTo('session', session.id);
        },

        goto_test: function(test) {
            this.transitionTo('test', test.id);
        },

        loading: function(transition) {
            let controller = this.controllerFor('application');
            controller.set('loading', true);
            transition.promise.finally(function() {
                controller.set('loading', false);
            });
        }
    }
});
