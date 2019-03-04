import Component from "@ember/component";
import { lower_case } from "../../utils/computed";

export default Component.extend({
  status: null,
  session_model: null,

  status_lower: lower_case("status"),

  spaced: true,
  classNames: "status-icon",
  classNameBindings: ["spaced:spaced", "status_lower"],
  tagName: "span",
});
