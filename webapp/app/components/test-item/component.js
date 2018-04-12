import { oneWay, equal } from '@ember/object/computed';
import { inject as service } from '@ember/service';
import Component from '@ember/component';

export default Component.extend({
  display: service(),
  api: service(),
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
  }.property("test"),
  actions: {
    toggle_starred: function() {
      let self = this;
      return this.get("api")
        .call("toggle_starred", { object_id: this.get("test.id") })
        .then(function() {
            return self.get('test').reload();
        });
    },
  }
});
