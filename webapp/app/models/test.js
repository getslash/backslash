import DS from "ember-data";
import HasLogicalId from "../mixins/has-logical-id";
import HasComputedStatus from "../mixins/has-computed-status";

export default DS.Model.extend(HasLogicalId, HasComputedStatus, {
  session_display_id: DS.attr(),

  has_any_error: function() {
    return this.get("num_errors") || this.get("num_failures");
  }.property("num_failures", "num_errors"),

  start_time: DS.attr("number"),
  end_time: DS.attr("number"),
  duration: DS.attr("number"),
  status: DS.attr("string"),

  num_errors: DS.attr("number"),
  num_warnings: DS.attr("number"),
  num_comments: DS.attr("number"),

  test_info_id: DS.attr("number"),

  test_index: DS.attr("number"),

  type: DS.attr(),

  user_display_name: DS.attr(),
  user_email: DS.attr(),

  first_error: DS.attr(),
  last_comment: DS.attr(),

  scm: DS.attr(),
  scm_revision: DS.attr(),
  scm_dirty: DS.attr(),
  scm_local_branch: DS.attr(),
  scm_remote_branch: DS.attr(),
  file_hash: DS.attr(),

  skip_reason: DS.attr(),

  info: DS.attr(),
  session_id: DS.attr("number"),

  variation: DS.attr(),
  parameters: DS.attr(),
  subjects: DS.attr(),

  is_success: function() {
    return this.get("status") === "SUCCESS";
  }.property("status"),

  is_skipped: function() {
    return this.get("status") === "SKIPPED";
  }.property("status"),

  is_running: function() {
    return this.get("status") === "RUNNING";
  }.property("status"),

  is_session_abandoned: DS.attr("boolean")
});
