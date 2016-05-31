import Ember from 'ember';

export default Ember.Route.extend({

    setupController(controller, ...args) {
	this._super(controller, ...args);
	controller.reset();

    }
});
