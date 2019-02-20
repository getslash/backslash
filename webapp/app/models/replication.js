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
  lag_seconds: DS.attr("number"),
  last_replicated_timestamp: DS.attr(),

  lagging: computed('lag_seconds', function() {
    let lag_seconds = this.get('lag_seconds');
    if (lag_seconds === null) {
      return true;
    }
    return lag_seconds > 5 * 60;
  }),
});
