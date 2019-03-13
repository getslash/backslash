import EmberObject from "@ember/object";
import Component from "@ember/component";

const _MAX_VALUE_SIZE = 100;

export default Component.extend({
  additional: null,
  metadata: null,

  related_entities: null,

  related_groups: function() {
    let related = this.get("related_entities");
    if (!related) {
      return {};
    }
    let returned = {};
    related.map(function(entity) {
      let existing = returned[entity.get("entity_type")];
      if (existing === undefined) {
        existing = returned[entity.get("entity_type")] = [];
      }
      existing.push(entity.get("name"));
    });
    return returned;
  }.property("related_entities"),

  all_metadata: function() {
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
        returned.push(
          EmberObject.create({
            name: attrname,
            value: value,
            short_value: short_value,
            expanded: false,
            expandable: short_value !== value,
          })
        );
      }
      returned.sort(function(first, second) {
        return first.get("name").localeCompare(second.get("name"));
      });
      return returned;
    });
    return returned;
  }.property("additional", "metadata"),
});
