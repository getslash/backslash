import { hash } from 'rsvp';
import Route from '@ember/routing/route';
import ComplexModelRoute from "../../mixins/complex-model-route";

export default Route.extend(ComplexModelRoute, {

  model() {
    let self = this;
    let session_model = this.modelFor("session").session_model;
    return hash({
      session_model: session_model,
      related_entities: self.store.query('entity', {session_id: session_model.id, page_size: 100}),
      metadata: this.modelFor("session").metadata,
    });
  }
});
