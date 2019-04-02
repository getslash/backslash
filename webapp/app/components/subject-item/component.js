import Component from "@ember/component";
import { oneWay } from "@ember/object/computed";
import { inject as service } from "@ember/service";

export default Component.extend({
  classNames: "item clickable",
  subject: oneWay("item"),
  router: service(),

  click() {
    this.get("router").transitionTo("subject", this.get("item.name"));
  },
});
