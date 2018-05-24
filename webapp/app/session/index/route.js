import { hash } from 'rsvp';
import Route from '@ember/routing/route';
import AuthenticatedRouteMixin
  from "ember-simple-auth/mixins/authenticated-route-mixin";
import RefreshableRouteMixin from "../../mixins/refreshable-route";
import StatusFilterableRoute from "../../mixins/status-filterable/route";
import SearchRouteMixin from "../../mixins/search-route";

export default Route.extend(
  AuthenticatedRouteMixin,
  RefreshableRouteMixin,
  StatusFilterableRoute,
  SearchRouteMixin,
  {
    title: "Session",
    queryParams: {
      show_planned: {
        refreshModel: true
      },
      search: {
        replace: true,
        refreshModel: true
      },
    },

    model: function(params) {
      let session = this.modelFor("session").session_model;
      const session_id = parseInt(session.id);

      let query_params = {
        session_id: session_id,
        page: params.page,
        page_size: params.page_size
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
      return hash({
        session_model: session,
        tests: this.store.query("test", query_params),
        filters: filters
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

    setupController: function(controller, model) {
      this._super(controller, model);
      controller.set("error", null);
      let parent_controller = this.controllerFor("session");
      parent_controller.set("test_filters", model.filters);
      controller.setProperties(model);
    },
    resetController(controller, isExiting) {
      if (isExiting) {
        // isExiting would be false if only the route's model was changing
        controller.set("search", "");
        controller.set("entered_search", "");
        controller.setProperties({
          show_successful: true,
          show_unsuccessful: true,
          show_abandoned: true,
          show_skipped: true,
          show_planned: false,
        });
      }
    },
  }
);
