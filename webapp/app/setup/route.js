import Ember from 'ember';

export default Ember.Route.extend({
    setupController(controller) {
	this._super(controller, ...arguments);
	controller.set('config', {});
    },
});
