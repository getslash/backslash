import { assign } from '@ember/polyfills';
import Component from '@ember/component';

export default Component.extend({
  tagName: "span",
  classNames: ["test-name"],

  display_params: function() {
    let params = this.get("parameters");
    if (!params) {
      return this.get("variation");
    }

    let returned = assign({}, this.get("variation"), params);
    return returned;
  }.property("parameters", "variation")
});
