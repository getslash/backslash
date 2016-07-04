import Ember from 'ember';
import ApplicationRouteMixin from 'ember-simple-auth/mixins/application-route-mixin';
import config from '../config/environment';

export default Ember.Route.extend(ApplicationRouteMixin, {

    api: Ember.inject.service(),
    session: Ember.inject.service(),

    title(tokens) {
        return tokens.join(' - ') + ' - Backslash';
    },

    model() {
        return Ember.RSVP.hash({
            app_config: this.get('api').call('get_app_config').then(r => r.result),
        });
    },

    afterModel(model) {
	let cfg = config.torii;
	cfg.providers["google-oauth2"].apiKey = model.app_config.oauth2_client_id;
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
        if (self.get('session.data.authenticated')) {
            return self.store.find('user', 'self').then(function(u) {
                self.set('session.data.authenticated.current_user', u);
            }).catch(function() {
                let s = self.get('session');
                if (s !== undefined && s.get('isAuthenticated')) {
                    s.invalidate();
                }
            });
        }
    },

    setupController(controller, model) {
        controller.setProperties(model);
    },

    actions: {

        loading: function(transition) {
            let controller = this.controllerFor('application');
            controller.set('loading', true);
            transition.promise.finally(function() {
                controller.set('loading', false);
            });
        },
    },

});
