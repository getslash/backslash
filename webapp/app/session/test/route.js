import Ember from 'ember';

import ComplexModelRoute from '../../mixins/complex-model-route';

export default Ember.Route.extend(ComplexModelRoute, {

    parent_controller: function() {
	return this.controllerFor('session');
    }.property(),

    setupController(controller, model) {
	this._super(...arguments);
	this.get('parent_controller').set('current_test', model.test_model);
    },

    deactivate() {
	this.get('parent_controller').set('current_test', null);
    },

    model(params) {
	return Ember.RSVP.hash({
	    test_model: this.store.find('test', params.test_id),
	});
    },

});
