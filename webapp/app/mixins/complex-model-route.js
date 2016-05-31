import Ember from 'ember';

export default Ember.Mixin.create({
    setupController(controller, model, ...args) {
	this._super(controller, model, ...args);
	controller.setProperties(model);
    }
});
