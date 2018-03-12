import { oneWay, equal } from '@ember/object/computed';
import { inject as service } from '@ember/service';
import Component from '@ember/component';

export default Component.extend({
  display: service(),
  attributeBindings: ["href"],
  tagName: "a",
  classNames: ["item", "test", "clickable"],

  classNameBindings: [
    "test.computed_status",
    "test.has_any_error:unsuccessful"
  ],

  test: oneWay("item"),
  session_model: null,
  is_running: equal("test.computed_status", "running"),



  href: function() {
    let returned = `/#/sessions/${this.get("test.session_display_id")}/tests/${this.get("test.display_id")}`;
    if (this.get("test.has_any_error")) {
      returned += "/errors";
    }
    return returned;
  }.property("test")
});
