import Controller from "@ember/controller";
import { computed } from "@ember/object";
import { inject } from "@ember/service";

export default Controller.extend({
  user_prefs: inject(),
  show_session_overview: null,

  session_overview_visible: computed(
    "show_session_overview",
    "user_prefs.show_test_session_overviews",
    function() {
      let show_overview = this.get("show_session_overview");
      if (show_overview !== null) {
        return show_overview;
      }

      return this.get("user_prefs.show_test_session_overviews");
    }
  ),
});
