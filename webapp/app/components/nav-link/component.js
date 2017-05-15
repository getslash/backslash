import Ember from "ember";

export default Ember.Component.extend({
  to: null,
  tagName: "li",
  path_tracker: Ember.inject.service(),
  current_path: Ember.computed.oneWay("path_tracker.path"),

  classNameBindings: ["is_active:active"],

  is_active: false
});
