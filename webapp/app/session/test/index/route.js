import { hash } from "rsvp";
import Route from "@ember/routing/route";

import ComplexModelRoute from "../../../mixins/complex-model-route";

export default Route.extend(ComplexModelRoute, {
  model() {
    let session_model = this.modelFor("session").session_model;
    let test_model = this.modelFor("session.test").test_model;
    let test_metadata = this.modelFor("session.test").test_metadata;
    return hash({
      session_model: session_model,
      test_model: test_model,
      metadata: test_metadata,
    });
  },
});
