import Ember from "ember";
import AuthenticatedRouteMixin
  from "ember-simple-auth/mixins/authenticated-route-mixin";
import PaginatedRoute from "../../mixins/paginated-route";
import ComplexModelRoute from "../../mixins/complex-model-route";

export default Ember.Route.extend(
  AuthenticatedRouteMixin,
  ComplexModelRoute,
  PaginatedRoute,
  {
    model: function({page, page_size}) {
      const parent = this.modelFor("session").session_model;
      return Ember.RSVP.hash({
        session: this.modelFor("session").session_model,
        errors: this.store.query("error", {
          session_id: parent.id,
          interruptions: true,
          page: page,
          page_size: page_size,
        })
      });
    }
  }
);
