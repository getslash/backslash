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
    let variation = this.get("test.variation");
    let params = this.get("test.parameters");
    if (!params) {
      params = variation;
    }
    if (variation) {
      for (var key in variation) {
        if (!Number.isInteger(variation[key])) {
          params[key] = variation[key];
        }
      }
    }

    let returned = assign({}, this.get("variation"), params);
    return returned;
  }),

  click(e) {
    e.stopPropagation();
    return this.get("router").transitionTo("test", this.get("test.display_id"));
  },
});
