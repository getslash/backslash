import Component from "@ember/component";
import { computed } from "@ember/object";

const _MAX_VALUE_SIZE = 100;

export default Component.extend({
  additional: null,
  metadata: null,

  related_entities: null,

  all_metadata: computed("additional", "metadata", function() {
    let returned = [];

    [this.get("additional"), this.get("metadata")].forEach(function(obj) {
      for (var attrname in obj) {
        let value = obj[attrname];
        if (typeof value === "object") {
          value = JSON.stringify(value, null, 2);
        }
        let short_value = value;
        if (value.length > _MAX_VALUE_SIZE) {
          short_value = short_value.substr(0, _MAX_VALUE_SIZE) + "...";
        }
        returned.push({
          name: attrname.replace("::", " "),
          multiline: typeof value == "string" && value.indexOf("\n") !== -1,
          value: value,
        });
      }
      returned.sort(function(first, second) {
        return first.name.localeCompare(second.name);
      });
      return returned;
    });
    return returned;
  }),
});
