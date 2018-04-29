import { oneWay } from '@ember/object/computed';
import { computed } from '@ember/object';
import { inject as service } from '@ember/service';
import Controller from '@ember/controller';


/* global moment */

export default Controller.extend({
    user_prefs: service(),
    saving: false,

    time_format: oneWay("model.time_format"),

    init() {
        this._super(...arguments);

        this.set('time_formats', [
            "DD/MM/YYYY HH:mm:ss",
            "DD/MM/YYYY HH:mm",
            "DD.MM.YYYY HH:mm:ss",
            "DD.MM.YYYY HH:mm",
            "YYYY-MM-DD HH:mm:ss"
        ]);

        this.set('start_pages', [
            "default", "my sessions"
        ]);
    },

    start_page: oneWay("model.start_page"),



    display_time_formats: computed('time_formats', function() {
        let returned = [];
        let formats = this.get("time_formats");

        let now = moment();

        for (let fmt of formats) {
            returned.push(now.format(fmt));
        }

        return returned;
    }),

    actions: {
        choose_option: function(option_name, value) {
            let self = this;

            self.set("saving", true);
            self
                .get("user_prefs")
                .set_pref(option_name, value)
                .then(function(new_value) {
                    self.set(option_name, new_value);
                })
                .always(function() {
                    self.set("saving", false);
                });
        }
    }
});
