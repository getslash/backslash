import { alias, oneWay, and } from "@ember/object/computed";
import { computed } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@ember/component";

export default Component.extend({
  display: service(),
  _router: service("router"),
  user_prefs: service(),

  tagName: "a",
  classNames: "item session clickable d-block nodecoration",
  classNameBindings: ["session.status_lowercase"],
  show_labels: true,

  attributeBindings: ["session.display_id:data-session-id", "href"],

  session: alias("item"),

  in_pdb: oneWay("session.in_pdb"),
  interrupted: and("item.finished_running", "item.has_tests_left_to_run"),

  href: computed("session.display_id", function() {
    return this._router.urlFor("session", this.get("session.display_id"));
  }),

  has_any_error: computed(
    "item.{num_failed_tests,num_error_tests,num_errors}",
    function() {
      let item = this.get("item");

      return (
        item.get("num_error_tests") ||
        item.get("num_failed_tests") ||
        item.get("num_errors")
      );
    }
  ),
});
