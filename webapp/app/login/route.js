import { hash } from 'rsvp';
import { inject as service } from '@ember/service';
import Route from '@ember/routing/route';
import UnauthenticatedRouteMixin
  from "ember-simple-auth/mixins/unauthenticated-route-mixin";

export default Route.extend(UnauthenticatedRouteMixin, {
  runtime_config: service(),

  model() {
    return hash({
      runtime_config: this.get("runtime_config").get_all()
    });
  },

  setupController(controller, model) {
    this._super(controller, model, ...arguments);
    controller.set("torii", this.get("torii"));
    controller.setProperties(model);
  }
});
