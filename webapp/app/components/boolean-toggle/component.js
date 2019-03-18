import Component from "@ember/component";
import { computed } from "@ember/object";

export default Component.extend({
  value: null,
  action: null,
  tagName: "button",

  classNames: "btn btn-secondary ml-2",
  classNameBindings: "class_name",

  class_name: computed("value", function() {
    return this.get("value") ? "btn-success" : "btn-secondary";
  }),

  click() {
    this.get("action")();
    return false;
  },
});
