import Ember from "ember";

export default Ember.Controller.extend({
  additional_metadata: function() {
    return { "Ran from": this.get("session_model.hostname") };
  }.property("session_model.hostname")
});
