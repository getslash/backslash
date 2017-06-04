import Ember from "ember";

import ComplexModelRoute from "../../mixins/complex-model-route";

export default Ember.Route.extend(ComplexModelRoute, {

  api: Ember.inject.service(),


  parent_controller: function() {
    return this.controllerFor("session");
  }.property(),

  setupController(controller, model) {
    this._super(...arguments);
    this.get("parent_controller").set("current_test", model.test_model);
  },

  model(params) {
    let self = this;
    let session = self.modelFor("session").session_model;

    return self.store.find('test', params.test_id).then(function(test) {

      return Ember.RSVP.hash({
        session_model: session,
        test_metadata: (self.get("api")
                        .call("get_metadata", {
                          entity_type: "test",
                          entity_id: parseInt(test.id)
                        })
                        .then(r => r.result)),
        test_model: test,
      });

    });
  },

});
