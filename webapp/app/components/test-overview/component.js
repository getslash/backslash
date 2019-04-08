import Component from "@ember/component";
import EmberObject from "@ember/object";
import { computed } from "@ember/object";
import { oneWay } from "@ember/object/computed";
import { inject as service } from "@ember/service";

export default Component.extend({
  runtime_config: service(),

  classNames: "p-3 test-overview overview",

  session_model: null,
  test_metadata: null,
  test_model: null,

  slash_tags: computed("test_metadata", function() {
    let metadata = this.get("test_metadata");
    if (!metadata) {
      return null;
    }
    let tags = metadata["slash::tags"];
    if (!tags) {
      return null;
    }

    let returned = [];
    for (const [name, value] of Object.entries(tags.values)) {
      returned.push({ name: name, value: value });
    }
    for (let name of tags.names) {
      if (tags.values.hasOwnProperty(name)) {
        continue;
      }
      returned.push({ name: name, value: null });
    }
    return returned;
  }),

  metadata_links: computed("test_metadata", function() {
    let returned = [];
    let metadata = this.get("test_metadata");

    for (let link of this.get("runtime_config").get_cached(
      "test_metadata_links"
    )) {
      let value = metadata[link.key];
      if (value) {
        returned.push({
          name: link.name,
          url: value,
          icon: link.icon,
        });
      }
      return returned;
    }
  }),

  metadata_display_items: computed(function() {
    return this.get("runtime_config").get_cached("test_metadata_display_items");
  }),

  scm_details: computed("test_model", function() {
    let self = this;
    let test_model = self.get("test_model");

    if (!test_model.get("scm")) {
      return {};
    }

    let returned = EmberObject.create({
      Revision: test_model.get("scm_revision"),
      "File Hash": test_model.get("file_hash"),
      "Local Branch": test_model.get("scm_local_branch"),
      "Remote Branch": test_model.get("scm_remote_branch"),
    });
    return returned;
  }),
});
