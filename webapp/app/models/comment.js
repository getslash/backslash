import DS from "ember-data";
import Ember from "ember";

export default DS.Model.extend({
  user_id: DS.attr("number"),
  comment: DS.attr(),
  timestamp: DS.attr(),
  edited: DS.attr("boolean"),
  user: DS.attr(),
  user_email: DS.attr(),

  can: DS.attr(),

  deleted: DS.attr("boolean"),

  has_text: function() {
    return Ember.$.trim(this.get("comment")) !== "";
  }.property("comment"),

  is_committed: function() {
    return !this.get("edited");
  }.property("edited")
});
