import Ember from "ember";

import ComplexModelRoute from "../../../mixins/complex-model-route";

export default Ember.Route.extend(ComplexModelRoute, {

  api: Ember.inject.service(),

  model() {
    let session_model = this.modelFor("session").session_model;
    let test_model = this.modelFor("session.test").test_model;
    let test_metadata = this.modelFor("session.test").test_metadata;
    return Ember.RSVP.hash({
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
