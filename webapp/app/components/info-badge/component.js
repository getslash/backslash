import Component from "@ember/component";
import { computed } from "@ember/object";

export default Component.extend({
  tagName: "small",
  classNames: "badge p-1 border",
  classNameBindings: ["_border", "_bg_color", "_fg_color"],
  color: "light",
  border_color: "dark",
  fg: "black-50",
  text: null,

  _fg_color: computed("fg", function() {
    return `text-${this.get("fg")}`;
  }),
  _bg_color: computed("color", function() {
    return `bg-${this.get("color")}`;
  }),
  _border: computed("border_color", function() {
    return `border-${this.get("border_color")}`;
  }),
});
