import Ember from 'ember';
import UnauthenticatedRouteMixin from 'ember-simple-auth/mixins/unauthenticated-route-mixin';

export default Ember.Route.extend(UnauthenticatedRouteMixin, {

    runtime_config: Ember.inject.service(),

    model() {
	return Ember.RSVP.hash({
	    runtime_config: this.get('runtime_config').get_all(),
	});
    },

    setupController(controller, model) {
        this._super(controller, model, ...arguments);
        controller.set('torii', this.get('torii'));
	controller.setProperties(model);
    }

});
