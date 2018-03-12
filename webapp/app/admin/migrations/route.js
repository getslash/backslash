import { hash } from 'rsvp';
import Route from '@ember/routing/route';

import ComplexModelRoute from "../../mixins/complex-model-route";
import PollingRoute from "../../mixins/polling-route";

export default Route.extend(ComplexModelRoute, PollingRoute, {

  should_auto_refresh() {
    return true;
  },

  model() {
    return hash({
      migrations: this.store.query('migration', {}),
    });
  },
});
