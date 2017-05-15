import Ember from "ember";

export default Ember.Mixin.create({
  setupController(controller, model) {
    this._super(...arguments);
    controller.setProperties(model);
  }
});
