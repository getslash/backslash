import Ember from "ember";

export default Ember.Component.extend({
  classNames: ["container-fluid"],
  show_breakdown: true,
  session_model: null,
  user: null,
  metadata: null,
  runtime_config: Ember.inject.service(),

  metadata_display_items: function() {
    let returned = this.get('runtime_config').get_cached('session_metadata_display_items');
    return returned;
  }.property(),

  not_complete: Ember.computed.and(
    "session_model.finished_running",
    "session_model.has_tests_left_to_run"
  )
});
