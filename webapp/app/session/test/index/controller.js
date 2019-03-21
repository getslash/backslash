import EmberObject from "@ember/object";
import { computed } from "@ember/object";
import Controller from "@ember/controller";

import RelativeItemJump from "../../../mixins/relative-item-jump";

export default Controller.extend(RelativeItemJump, {
  additional_metadata: computed(function() {
    return {};
  }),

  params: computed("test_model.{parameters,variation}", function() {
    let params = this.get("test_model.parameters");
    if (!params) {
      params = this.get("test_model.variation");
    }
    let returned = [];
    for (let [key, value] of Object.entries(params || {})) {
      returned.push({ name: key, value: value });
    }
    return returned;
  }),
});
