import { hash } from 'rsvp';

import PaginatedFilteredRoute from "../routes/paginated_filtered_route";
import AuthenticatedRouteMixin
  from "ember-simple-auth/mixins/authenticated-route-mixin";
import ScrollToTopMixin from "../mixins/scroll-top";
import StatusFilterableRoute from "../mixins/status-filterable/route";

export default PaginatedFilteredRoute.extend(
  AuthenticatedRouteMixin,
  ScrollToTopMixin,
  StatusFilterableRoute,
  {
    titleToken(model) {
      return model.subject.get("name");
    },

    queryParams: {
      page: {
        refreshModel: true
      },
      page_size: {
        refreshModel: true
      }
    },

    model(params) {
      let query_params = {
        subject_name: params.name,
        page: params.page,
        page_size: params.page_size
      };
      this.transfer_filter_params(params, query_params);
      return hash({
        subject: this.store.find("subject", params.name),
        sessions: this.store.query("session", query_params)
      });
    },

    setupController(controller, model) {
      this._super(controller, model);
      controller.setProperties(model);
      controller.set("page", model.sessions.get("meta.page"));
    },

    renderTemplate() {
      this._super(...arguments);
      this.render("filter-controls", {
        into: "subject",
        outlet: "filter-controls"
      });
    }
  }
);
