import Ember from 'ember';
import ApplicationRouteMixin from 'ember-simple-auth/mixins/application-route-mixin';

export default Ember.Route.extend(ApplicationRouteMixin, {

    title(tokens) {
        return tokens.join(' - ') + ' - Backslash';
    },

    model() {
        return Ember.RSVP.hash({
            app_config: this.api.call('get_app_config').then(r => r.result),
        });
    },

    beforeModel() {
        this.load_current_user();
    },

    sessionAuthenticated() {
        this._super(...arguments);
        this.load_current_user();
    },

    load_current_user() {
        let self = this;
        if (self.get('session.authenticated')) {
            return self.store.find('user', 'self').then(function(u) {
                self.set('session.authenticated.data.current_user', u);
            }).catch(() => this.get('session').invalidate());
        }
    },

    setupController(controller, model) {
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
        },
    },

});
