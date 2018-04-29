import Route from '@ember/routing/route';
import AuthenticatedRouteMixin
  from "ember-simple-auth/mixins/authenticated-route-mixin";
import RefreshableRouteMixin from "../mixins/refreshable-route";

export default Route.extend(
  AuthenticatedRouteMixin,
  RefreshableRouteMixin,
  {
    queryParams: {
      page: {
        refreshModel: true
      },
      page_size: {
        refreshModel: true
      },
      filter: {
        refreshModel: true
      }
    },

    resetController(controller) {
      controller.set("filter", undefined);
      controller.set("page", 1);
    }
  }
);
