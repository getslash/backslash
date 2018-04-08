import { assign } from '@ember/polyfills';
import Component from '@ember/component';

export default Component.extend({
  tagName: "span",
  classNames: ["test-name"],

  display_params: function() {
    let variation = this.get("variation");
    let params = this.get("parameters");
    if (!params) {
      params = variation;
    }
    if (variation) {
      for (var key in variation) {
        if (!Number.isInteger(variation[key])) {
          params[key] = variation[key]
        }
      }
    }

    let returned = assign({}, this.get("variation"), params);
    return returned;
  }.property("parameters", "variation")
});
