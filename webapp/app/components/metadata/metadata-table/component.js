import Ember from "ember";

const _MAX_VALUE_SIZE = 100;

export default Ember.Component.extend({
  additional: {},
  metadata: {},

  related_entities: null,

  related_groups: function() {
    let related = this.get("related_entities");
    if (!related) {
      return {};
    }
    let returned = {};
    related.map(function(entity) {
      let existing = returned[entity.get('entty_type')];
      if (existing === undefined) {
        existing = returned[entity.get('entity_type')] = [];
      }
      existing.push(entity.get('name'));
    });
    return returned;
  }.property("related_entities"),


  all_metadata: function() {
    let returned = [];

    [this.get("additional"), this.get("metadata")].forEach(function(obj) {
      for (var attrname in obj) {
        let value = obj[attrname];
        if (typeof(value) === "object") {
          value = JSON.stringify(value, null, 2);
        }
        let short_value = value;
        if (value.length > _MAX_VALUE_SIZE) {
          short_value = short_value.substr(0, _MAX_VALUE_SIZE) + '...';
        }
        returned.push(Ember.Object.create({
          name: attrname,
          value: value,
          short_value: short_value,
          expanded: false,
          expandable: short_value !== value,
        }));
      }
      return returned;
    });
    return returned;
  }.property("additional", "metadata"),

  slash_commandline: function() {
    let returned = this.get("metadata.slash.commandline");

    if (returned === undefined) {
      returned = this.get("metadata")["slash::commandline"];
    }
    return returned;
  }.property("metadata"),

  slash_version: function() {
    let metadata = this.get("metadata") || {};
    let returned = metadata["slash::version"];
    if (!returned && metadata.slash !== undefined) {
      returned = metadata.slash.version;
    }
    return returned;
  }.property("metadata"),

  slash_tags: function() {
    let metadata = this.get("metadata");

    let returned = metadata["slash::tags"];
    return returned;
  }.property("metadata"),

  slash_tags_without_values: function() {
    let tags = this.get("slash_tags");
    let returned = [];

    for (let tag of tags.names) {
      if (!tags.values.hasOwnProperty(tag)) {
        returned.push(tag);
      }
    }
    return returned;
  }.property("slash_tags")
});
