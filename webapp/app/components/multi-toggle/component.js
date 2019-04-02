import { computed } from "@ember/object";
import Component from "@ember/component";

export default Component.extend({
  saving: false,

  display: null,
  options: null,

  normalized_options: computed("options", "display", function() {
    let display = this.get("display");
    let options = this.get("options");

    if (!display) {
      display = options;
    }

    let returned = [];

    for (let i = 0; i < options.length; ++i) {
      returned.push({ option: options[i], display: display[i] });
    }
    return returned;
  }),

  actions: {
    choose: function(option) {
      this.sendAction("action", option);
    },
  },
});
