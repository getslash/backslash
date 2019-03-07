import { alias, oneWay, and } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import Component from "@ember/component";

export default Component.extend({
  display: service(),
  router: service(),
  classNames: "item session clickable",
  classNameBindings: ["session.status_lowercase"],
  show_labels: true,

  attributeBindings: ["session.display_id:data-session-id"],

  session: alias("item"),

  in_pdb: oneWay("session.in_pdb"),
  interrupted: and("item.finished_running", "item.has_tests_left_to_run"),

  click() {
    return this.get("router").transitionTo(
      "session",
      this.get("session.display_id")
    );
  },

  has_any_error: function() {
    let item = this.get("item");

    return (
      item.get("num_error_tests") ||
      item.get("num_failed_tests") ||
      item.get("num_errors")
    );
  }.property(
    "item.num_failed_tests",
    "item.num_error_tests",
    "item.num_errors"
  ),
});
