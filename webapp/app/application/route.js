import Ember from 'ember';
import ApplicationRouteMixin from 'ember-simple-auth/mixins/application-route-mixin';
import config from '../config/environment';

export default Ember.Route.extend(ApplicationRouteMixin, {

    api: Ember.inject.service(),
    session: Ember.inject.service(),
    runtime_config: Ember.inject.service(),
    user_prefs: Ember.inject.service(),

    title(tokens) {
        return tokens.join(' - ') + ' - Backslash';
    },

    model() {
        return Ember.RSVP.hash({
            runtime_config: this.get('runtime_config').get_all(),
        });
    },

    afterModel(model) {

        if (model.runtime_config.setup_needed) {
            this.transitionTo('setup');
        } else {
            let cfg = config.torii;
            cfg.providers["google-oauth2"].apiKey = model.runtime_config.google_oauth2_client_id;
            this.load_current_user();
        }
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
                return self.get('user_prefs').get_all();
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
        controller.set('version', model.runtime_config.version);
    },

});
