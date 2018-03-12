import { hash } from 'rsvp';
import Route from '@ember/routing/route';
import AuthenticatedRouteMixin
  from "ember-simple-auth/mixins/authenticated-route-mixin";
import PaginatedRoute from "../../../mixins/paginated-route";
import ComplexModelRoute from "../../../mixins/complex-model-route";

export default Route.extend(
  AuthenticatedRouteMixin,
  PaginatedRoute,
  ComplexModelRoute,
  {
    model: function({page, page_size}) {
      const parent = this.modelFor("session.test");
      return hash({
        test_model: parent.test_model,
        session_model: parent.session_model,
        errors: this.store.query("error", {
          interruptions: true,
          test_id: parent.test_model.id,
          page: page,
          page_size: page_size,
        })
      });
    }
  }
);
