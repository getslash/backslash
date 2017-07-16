import Ember from 'ember';

import ComplexModelRoute from "../../mixins/complex-model-route";
import PollingRoute from "../../mixins/polling-route";

export default Ember.Route.extend(ComplexModelRoute, PollingRoute, {

  should_auto_refresh() {
    return true;
  },

  model() {
    return Ember.RSVP.hash({
      migrations: this.store.query('migration', {}),
    });
  },
});
