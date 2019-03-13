import EmberObject from "@ember/object";
import Controller from "@ember/controller";

import RelativeItemJump from "../../../mixins/relative-item-jump";

export default Controller.extend(RelativeItemJump, {
  additional_metadata: function() {
    return {};
  }.property("test_model"),

  params: function() {
    let params = this.get("test_model.parameters");
    if (params) {
      return params;
    }
    return this.get("test_model.variation");
  }.property("test_model"),
});
