import Ember from "ember";
import AuthenticatedRouteMixin
  from "ember-simple-auth/mixins/authenticated-route-mixin";
import PaginatedRoute from "../../../mixins/paginated-route";
import ComplexModelRoute from "../../../mixins/complex-model-route";

export default Ember.Route.extend(
  AuthenticatedRouteMixin,
  PaginatedRoute,
  ComplexModelRoute,
  {
    model: function({page, page_size}) {
      const parent = this.modelFor("session.test");
      return Ember.RSVP.hash({
        test_model: parent.test_model,
        session_model: parent.session_model,
        errors: this.store.query("error", {
          test_id: parent.test_model.id,
          page: page,
          page_size: page_size,
        })
      });
    }
  }
);
