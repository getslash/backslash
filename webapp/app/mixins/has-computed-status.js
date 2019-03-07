import { computed } from "@ember/object";
import { lower_case } from "../utils/computed";
import Mixin from "@ember/object/mixin";

export default Mixin.create({
  status_lowercase: lower_case("computed_status"),

  computed_status: computed(
    "status",
    "in_pdb",
    "is_abandoned",
    "is_session_abandoned",
    "num_skipped_tests",
    "num_interrupted_tests",
    "has_any_error",
    "is_running",
    function() {
      let status = this.get("status");
      if (!status) {
        return status;
      }

      status = status.toLowerCase();
      let interrupted =
        this.get("is_interrupted") || this.get("num_interrupted_tests");
      let running = this.get("is_running") || status === "running";

      if (
        (this.get("is_abandoned") || this.get("is_session_abandoned")) &&
        status === "running"
      ) {
        return "abandoned";
      }

      if (this.get("in_pdb")) {
        return "debugging";
      }

      if (!interrupted && running) {
        return "running";
      }

      if (
        !interrupted &&
        (this.get("has_any_error") ||
          ["error", "failure"].indexOf(status) !== -1)
      ) {
        return "failed";
      }

      if (interrupted) {
        return "interrupted";
      }

      if (status === "skipped") {
        return "skipped";
      }

      if (this.get("num_finished_tests") || status === "success") {
        return "success";
      }

      if (status === "planned") {
        return "planned";
      }

      return "finished";
    }
  ),
});
