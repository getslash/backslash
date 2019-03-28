import { oneWay } from "@ember/object/computed";
import { computed } from "@ember/object";
import { inject as service } from "@ember/service";
import Controller from "@ember/controller";

/* global moment */

export default Controller.extend({
  user_prefs: service(),
  saving: false,

  time_format: oneWay("model.time_format"),

  init() {
    this._super(...arguments);

    this.set("time_formats", [
      "DD/MM/YYYY HH:mm:ss",
      "DD/MM/YYYY HH:mm",
      "DD.MM.YYYY HH:mm:ss",
      "DD.MM.YYYY HH:mm",
      "YYYY-MM-DD HH:mm:ss",
    ]);

    this.set("start_pages", ["default", "my sessions"]);
  },

  display_time_formats: computed("time_formats", function() {
    let returned = [];
    let formats = this.get("time_formats");

    let now = moment();

    for (let fmt of formats) {
      returned.push(now.format(fmt));
    }
    return returned;
  }),

  _choose_option(option_name, value) {
    let self = this;
    self.set("saving", true);
    return self
      .get("user_prefs")
      .set_pref(option_name, value)
      .always(function() {
        self.set("saving", false);
      });
  },

  actions: {
    toggle_option: function(option_name) {
      return this._choose_option(
        option_name,
        !this.get("user_prefs").get(option_name)
      );
    },

    choose_option: function(option_name, value) {
      return this._choose_option(option_name, value);
    },
  },
});
