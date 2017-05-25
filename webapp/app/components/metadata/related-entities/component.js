import Ember from "ember";

export default Ember.Component.extend({
  related: null,

  groups: function() {
    let related = this.get("related");
    let returned = {};
    related.map(function(entity) {
      let existing = returned[entity.type];
      if (existing === undefined) {
        existing = returned[entity.type] = [];
      }
      existing.push(entity.name);
    });
    return returned;
  }.property("related")
});
