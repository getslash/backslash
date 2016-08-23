import Ember from 'ember';

import RefreshableRouteMixin from '../../mixins/refreshable-route';

export default Ember.Route.extend(RefreshableRouteMixin, {

    model() {
	let parent_model = this.modelFor('session');
	let session_model = parent_model.session_model;

	return Ember.RSVP.hash({
	    activity: this.store.query('activity', {session_id: session_model.id}),
	    session_model: session_model,
	});
    },

    setupController(controller, model) {
	this._super(...arguments);
	controller.setProperties(model);
    },

});
