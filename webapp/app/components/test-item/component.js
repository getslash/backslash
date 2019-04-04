import { assign } from "@ember/polyfills";
import { oneWay } from "@ember/object/computed";
import { computed } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@ember/component";

export default Component.extend({
  router: service(),

  attributeBindings: ["href"],
  classNames: "item test clickable",
  classNameBindings: "test.status_lowercase",

  session_model: null,
  test: oneWay("item"),

  display_params: computed("test.{parameters,variation}", function() {
    let seen = new Set();
    let returned = [];

    for (let params of [
      this.get("test.parameters"),
      this.get("test.variation"),
    ]) {
      if (!params) {
        continue;
      }
      for (var key in params) {
        if (params.hasOwnProperty(key)) {
          if (!seen.has(key)) {
            returned.push({ name: key, value: params[key] });
            seen.add(key);
          }
        }
      }
    }
    return returned;
  }),

  click(e) {
    e.stopPropagation();
    return this.get("router").transitionTo("test", this.get("test.display_id"));
  },
});
