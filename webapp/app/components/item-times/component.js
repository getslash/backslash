import { inject as service } from "@ember/service";
import { oneWay } from "@ember/object/computed";
import Component from "@ember/component";

/* global moment */

export default Component.extend({
  user_prefs: service(),

  classNames: ["times"],

  item: null,

  start: oneWay("item.start_time"),
  end: oneWay("item.end_time"),
  humanize: true,

  raw_times_text: function() {
    let start = this.get("start");
    let end = this.get("end");

    let returned = this._format(start) + " - ";
    if (!start) {
      return "Not started yet";
    }
    if (end) {
      returned += this._format(end);
    } else {
      returned += "...";
    }

    return returned;
  }.property("start", "end"),

  humanized_text: function() {
    let start = this.get("start");
    let end = this.get("end");
    if (!start) {
      return "Not started yet";
    }
    if (!end) {
      return "Started " + this._humanize(start);
    }
    return "Finished " + this._humanize(end);
  }.property("start", "end"),

  _humanize(t) {
    let now = moment();
    t = moment.unix(t);

    if (t.isAfter(now)) {
      t = now;
    }
    return t.fromNow();
  },

  _format(t) {
    const format = this.get("user_prefs").get_cached("time_format");
    return moment.unix(t).format(format);
  },
});
