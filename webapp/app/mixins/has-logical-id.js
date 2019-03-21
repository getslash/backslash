import Mixin from "@ember/object/mixin";
import DS from "ember-data";
import { computed } from "@ember/object";

export default Mixin.create({
  logical_id: DS.attr(),

  display_id: computed("logical_id", function() {
    let logical_id = this.get("logical_id");
    if (logical_id !== null) {
      return logical_id;
    }
    return this.get("id");
  }),
});
