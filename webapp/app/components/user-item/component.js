import { oneWay } from "@ember/object/computed";
import Component from "@ember/component";
import { inject as service } from "@ember/service";

export default Component.extend({
  classNames: ["item", "clickable"],
  user: oneWay("item"),
  router: service(),

  click() {
    return this.get("router").transitionTo("user", this.get("item.email"));
  },
});
