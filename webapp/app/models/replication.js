import DS from "ember-data";
import { computed } from "@ember/object";

export default DS.Model.extend({
  avg_per_second: DS.attr("number"),
  service_type: DS.attr("string"),
  url: DS.attr(),
  username: DS.attr(),
  password: DS.attr(),
  active: DS.attr("boolean"),
  backlog_remaining: DS.attr("number"),
  last_error: DS.attr(),
  paused: DS.attr(),
  last_replicated_timestamp: DS.attr(),

  last_replicated_timestamp_str: computed(
    "last_replicated_timestamp",
    function() {
      let timestamp = this.get("last_replicated_timestamp");
      if (timestamp) {
        return moment.unix(timestamp);
      }
    }
  ),

  time_remaining: computed("avg_per_second", "backlog_remaining", function() {
    let remaining = this.get("backlog_remaining");
    let avg = this.get("avg_per_second");
    if (!avg) {
      return 0;
    }
    let seconds_remaining = remaining / avg;
    if (seconds_remaining > 3600) {
      return `${Math.trunc(seconds_remaining / 3600)} hours`;
    } else if (seconds_remaining > 60) {
      return `${Math.trunc(seconds_remaining / 60)} minutes`;
    } else {
      return `${seconds_remaining} seconds`;
    }
  }),
});
