import Ember from 'ember';

import RefreshableRouteMixin from '../../../mixins/refreshable-route';

export default Ember.Route.extend(RefreshableRouteMixin, {

    model() {
	let test_model = this.modelFor('session.test').test_model;

	return Ember.RSVP.hash({
	    activity: this.store.query('activity', {test_id: parseInt(test_model.id)}),
	    test_model: test_model,
	});
    },

    setupController(controller, model) {
	this._super(...arguments);
	controller.setProperties(model);
    },

});
