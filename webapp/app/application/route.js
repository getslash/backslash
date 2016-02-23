import Ember from 'ember';
import ApplicationRouteMixin from 'ember-simple-auth/mixins/application-route-mixin';

export default Ember.Route.extend(ApplicationRouteMixin, {

    model() {

        return Ember.RSVP.hash({
            app_config: this.api.call('get_app_config').then(r => r.result),
        });
    },

    setupController(controller, model) {
        console.log('app config', model);
        controller.setProperties(model);
    },

    actions: {
        route_to(route_name, param) {
            this.transitionTo(route_name, param);
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
