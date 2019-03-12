import Component from "@ember/component";
import EmberObject from "@ember/object";
import { computed } from "@ember/object";
import { inject as service } from "@ember/service";

export default Component.extend({
  runtime_config: service(),

  classNames: "px-3 pb-3",

  session_model: null,
  test_metadata: null,
  test_model: null,

  didRender() {
    this.$().css("top", `${Ember.$(".session-overview").height()}px`);
  },

  metadata_links: computed("test_metadata", function() {
    let returned = [];
    let metadata = this.get("test_metadata");

    for (let link of this.get("runtime_config").get_cached(
      "test_metadata_links"
    )) {
      let value = metadata[link.key];
      if (value) {
        returned.push(
          EmberObject.create({
            name: link.name,
            url: value,
            icon: link.icon,
          })
        );
      }
      return returned;
    }
  }),

  metadata_display_items: computed(function() {
    return this.get("runtime_config").get_cached("test_metadata_display_items");
  }),
});
