import Component from "@ember/component";
import { inject as service } from "@ember/service";
import { computed } from "@ember/object";

export default Component.extend({
  router: service(),

  tagName: "span",

  label: "",

  classNames: "badge badge-pill",
  classNameBindings: ["label_color"],

  get_hash_code(s) {
    let hash = 0;
    if (s.length === 0) {
      return hash;
    }
    for (let i = 0; i < s.length; i++) {
      let char = s.charCodeAt(i);
      hash = (hash << 5) - hash + char;
      hash = hash & hash; // Convert to 32bit integer
    }
    hash ^= s.length;
    return Math.abs(hash);
  },

  label_color: computed("label", function() {
    let h = (this.get_hash_code(this.get("label")) % 5) + 1;
    return "label-color-" + h;
  }),

  click() {
    this.get("router").transitionTo("sessions", {
      queryParams: { search: `label=${this.get("label")}` },
    });
    return false;
  },
});
