import DS from "ember-data";
import Ember from "ember";
import HasLogicalId from "../mixins/has-logical-id";
import HasComputedStatus from "../mixins/has-computed-status";

export default DS.Model.extend(HasLogicalId, HasComputedStatus, {
  archived: DS.attr("boolean"),
  investigated: DS.attr("boolean"),

  start_time: DS.attr("number"),
  end_time: DS.attr("number"),

  is_abandoned: DS.attr("boolean"),

  in_pdb: DS.attr("boolean"),

  infrastructure: DS.attr(),

  num_error_tests: DS.attr("number"),
  num_interrupted_tests: DS.attr("number"),
  num_errors: DS.attr("number"),
  num_failed_tests: DS.attr("number"),
  num_finished_tests: DS.attr("number"),
  num_skipped_tests: DS.attr("number"),
  is_parent_session: DS.attr("boolean"),
  parent_logical_id: DS.attr("string"),
  child_id: DS.attr("string"),
  last_comment: DS.attr(),

  is_ok() {
    return !(this.get('num_errors') || this.get('num_error_tests') || this.get('num_failed_tests') || this.get('num_failures') || this.get('is_abandoned') || this.get('is_interrupted'));
  },

  num_successful_tests: function() {
    return (
      this.get("num_finished_tests") -
      this.get("num_error_tests") -
      this.get("num_failed_tests") -
      this.get("num_skipped_tests") -
      this.get("num_interrupted_tests")
    );
  }.property(
    "num_finished_tests",
    "num_error_tests",
    "num_failed_tests",
    "num_skipped_tests",
    "num_interrupted_tests"
  ),

  ran_all_tests: function() {
    if (this.get("total_num_tests") === null) {
      return true;
    }
    return (
      parseInt(this.get("num_finished_tests")) ===
      parseInt(this.get("total_num_tests"))
    );
  }.property("num_finished_tests", "total_num_tests"),

  has_tests_left_to_run: Ember.computed.not("ran_all_tests"),

  total_num_tests: DS.attr("number"),
  hostname: DS.attr(),

  num_warnings: DS.attr("number"),
  num_test_warnings: DS.attr("number"),
  num_comments: DS.attr("number"),

  next_keepalive: DS.attr("number"),
  related: DS.attr('raw'),
  labels: DS.attr(),

  total_num_warnings: function() {
    return this.get("num_warnings") + this.get("num_test_warnings");
  }.property("num_warnings", "num_test_warnings"),

  status: DS.attr("string"),

  is_interrupted: function() {
    return (
      (this.get("end_time") != null && this.get("has_tests_left_to_run")) ||
      this.get("status") === "INTERRUPTED" ||
      this.get("num_interrupted_tests")
    );
  }.property(
    "end_time",
    "has_tests_left_to_run",
    "status",
    "num_interrupted_tests"
  ),

  subjects: DS.attr(),

  type: DS.attr(),

  user_id: DS.attr(),
  user_email: DS.attr(),
  user_display_name: DS.attr(),

  real_email: DS.attr(),

  is_delegate: Ember.computed.notEmpty("real_email"),

  is_running: function() {
    return this.get("status") === "RUNNING";
  }.property("status"),

  finished_running: Ember.computed.not("is_running")
});
