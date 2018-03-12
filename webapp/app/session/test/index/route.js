import { hash } from 'rsvp';
import { inject as service } from '@ember/service';
import Route from '@ember/routing/route';

import ComplexModelRoute from "../../../mixins/complex-model-route";

export default Route.extend(ComplexModelRoute, {

  api: service(),

  model() {
    let session_model = this.modelFor("session").session_model;
    let test_model = this.modelFor("session.test").test_model;
    let test_metadata = this.modelFor("session.test").test_metadata;
    return hash({
      session_model: session_model,
      test_model: test_model,
      metadata: test_metadata,
      timings: this.get('api').call('get_timings', {test_id: parseInt(test_model.id)}).then(function(timings) {
        let returned = [];
        for (let name in timings.result) {
          returned.push({name: name, total: timings.result[name]});
        }
        return returned;
      }),
    });
  }
});
