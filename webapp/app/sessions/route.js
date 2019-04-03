import { hash } from "rsvp";
import { inject as service } from "@ember/service";

import PaginatedFilteredRoute from "../routes/paginated_filtered_route";
import AuthenticatedRouteMixin from "ember-simple-auth/mixins/authenticated-route-mixin";
import PollingRoute from "../mixins/polling-route";
import ScrollToTopMixin from "../mixins/scroll-top";
import SearchRouteMixin from "../mixins/search-route";
import StatusFilterableRoute from "./../mixins/status-filterable/route";

export default PaginatedFilteredRoute.extend(
  AuthenticatedRouteMixin,
  PollingRoute,
  ScrollToTopMixin,
  SearchRouteMixin,
  StatusFilterableRoute,
  {
    titleToken: "Sessions",

    user_prefs: service(),

    queryParams: {
      search: {
        replace: true,
        refreshModel: true,
      },
      page: {
        refreshModel: true,
      },
      page_size: {
        refreshModel: true,
      },
    },

    model(params) {
      let query_params = {
        page: params.page,
        filter: params.filter,
        page_size: params.page_size,
      };
      let filters = {};
      for (let key in params) {
        if (key.startsWith("show_")) {
          filters[key] = query_params[key] = params[key];
        }
      }
      if (params.search) {
        query_params.search = params.search;
      }

      let user_id = this.get_user_id_parameter();

      if (user_id !== undefined) {
        query_params.user_id = user_id;
      }
      return hash({
        sessions: this.store.query("session", query_params),
        filters: this.transfer_filter_params(params),
        __prefs: this.get("user_prefs").ensure_cache_populated(),
      }).catch(function(exception) {
        let message = exception.errors.get("firstObject");
        if (message) {
          if (message.detail === "The adapter operation was aborted") {
            return false;
          }
          if (message.status === "404") {
            return { error: message.title };
          }
          return { error: message };
        }
        throw exception; //reraise
      });
    },

    resetController(controller, isExiting) {
      if (isExiting) {
        // isExiting would be false if only the route's model was changing
        controller.set("search", "");
        controller.set("entered_search", "");
        let query_params = this.get("queryParams");
        for (let key in query_params) {
          if (key.startsWith("show_")) {
            controller.set(key, true);
          }
        }
      }
    },

    should_auto_refresh: function() {
      return true;
    },

    setupController(controller, model) {
      this._super(...arguments);
      controller.set("error", null);
      controller.setProperties(model);
      if (!model.error) {
        controller.set("page", model.sessions.get("meta.page"));
        controller.set("page_size", model.sessions.get("meta.page_size"));
      }
    },

    get_user_id_parameter: function() {
      return undefined;
    },
  }
);
