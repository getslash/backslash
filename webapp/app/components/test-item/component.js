import { assign } from "@ember/polyfills";
import { oneWay } from "@ember/object/computed";
import { computed } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@ember/component";

export default Component.extend({
  _router: service("router"),

  tagName: "a",
  attributeBindings: ["href"],
  classNames: "item test clickable d-block nodecoration",
  classNameBindings: ["test.status_lowercase", "compact_view:compact"],
  compact_view: false,

  session_model: null,
  test: oneWay("item"),

  href: computed("test.display_id", function() {
    return this._router.urlFor(
      "session.test",
      this.get("test.session_display_id"),
      this.get("test.display_id")
    );
  }),

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
});
