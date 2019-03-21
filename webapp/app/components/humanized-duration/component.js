import Component from "@ember/component";
import momentRange from "../../helpers/moment-range";
import { computed } from "@ember/object";

/* global moment */

export default Component.extend({
  tagName: "span",
  start_time: null,
  end_time: null,
  seconds: null,

  _corrected_end_time: computed("end_time", function() {
    return this.get("end_time") ? this.get("end_time") : moment().unix();
  }),

  _computed_duration: computed("start_time", "_corrected_end_time", function() {
    let start_time = this.get("start_time");

    if (start_time === undefined || start_time === null) {
      return null;
    }

    let end_time = this.get("_corrected_end_time");

    return moment.unix(end_time).diff(moment.unix(start_time)) / 1000;
  }),

  humanized_duration: computed("_computed_duration", "seconds", function() {
    let seconds = this.get("seconds");

    if (seconds === null || seconds === undefined) {
      seconds = this.get("_computed_duration");
    }

    if (!seconds) {
      return "-";
    }

    if (seconds < 60) {
      return `${seconds} seconds`;
    }

    let returned = moment.duration(seconds * 1000).humanize();
    if (!this.get("end_time")) {
      returned += " (not finished)";
    }
    return returned;
  }),
});
