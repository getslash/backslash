import Ember from "ember";

export default Ember.Mixin.create({
  computed_status: function() {
    let status = this.get("status");
    if (!status) {
      return status;
    }

    status = status.toLowerCase();
    let interrupted = this.get("is_interrupted");
    let running = this.get("is_running") || status === "running";

    if (
      (this.get("is_abandoned") || this.get("is_session_abandoned")) &&
      status === "running"
    ) {
      return "abandoned";
    }

    if (!interrupted && running) {
      return "running";
    }

    if (
      this.get("has_any_error") ||
      ["error", "failure"].indexOf(status) !== -1
    ) {
      return "failed";
    }

    if (interrupted) {
      return "interrupted";
    }

    if (this.get("num_skipped_tests") || status === "skipped") {
      return "skipped";
    }

    if (this.get("num_finished_tests") || status === "success") {
      return "success";
    }

    if (status === "planned") {
      return "planned";
    }

    return "finished";
  }.property(
    "status",
    "is_abandoned",
    "is_session_abandoned",
    "num_skipped_tests",
    "has_any_error",
    "is_running"
  )
});
