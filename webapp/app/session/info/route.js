import Ember from "ember";
import ComplexModelRoute from "../../mixins/complex-model-route";

export default Ember.Route.extend(ComplexModelRoute, {

  model() {
    let self = this;
    let session_model = this.modelFor("session").session_model;
    return Ember.RSVP.hash({
      session_model: session_model,
      related_entities: self.store.query('entity', {session_id: session_model.id, page_size: 100}),
      metadata: this.modelFor("session").metadata,
    });
  }
});
