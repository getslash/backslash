import { computed } from "@ember/object";
import Component from "@ember/component";

export default Component.extend({
  email: null,
  is_proxy: false,
  is_real: false,
  tagName: "img",

  attributeBindings: ["src"],
  classNames: ["avatar-image"],
  classNameBindings: ["is_proxy:proxy", "is_real:real"],

  src: computed("email", function() {
    let returned =
      "https://www.gravatar.com/avatar/" + window.md5(this.get("email"));
    returned += "?d=mm";
    return returned;
  }),
});
