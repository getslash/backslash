import Route from '@ember/routing/route';

export default Route.extend({
  setupController(controller) {
    this._super(controller, ...arguments);
    controller.set("config", {});
  }
});
