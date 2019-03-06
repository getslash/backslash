import { notEmpty } from "@ember/object/computed";
import Component from "@ember/component";

export default Component.extend({
  text: null,

  can_commit: notEmpty("text"),
});
