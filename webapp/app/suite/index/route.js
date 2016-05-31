import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default Ember.Route.extend(AuthenticatedRouteMixin, {

    model() {
	return Ember.RSVP.hash({
	    suite: this.modelFor('suite'),
	});

    },

    setupController(controller, model) {
	this._super(controller, model);
	controller.setProperties(model);
    }
});
