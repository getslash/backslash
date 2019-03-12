import Component from "@ember/component";
import { computed } from "@ember/object";
import { inject as service } from "@ember/service";

export default Component.extend({
  classNames: "p-3",
  session_model: null,
  user: null,

  runtime_config: service(),

  metadata_display_items: computed(function() {
    let returned = this.get("runtime_config").get_cached(
      "session_metadata_display_items"
    );
    return returned;
  }),
});
