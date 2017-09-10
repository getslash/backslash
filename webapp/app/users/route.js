import Ember from "ember";
import AuthenticatedRouteMixin
  from "ember-simple-auth/mixins/authenticated-route-mixin";
import SearchRoute from "../mixins/search-route";

export default Ember.Route.extend(AuthenticatedRouteMixin, SearchRoute, {
  titleToken: "Users",

  queryParams: {
    page: { refreshModel: true },
    search: {refreshModel: true },
    page_size: { refreshModel: true },
    sort: {
      refreshModel: true
    }
  },

  model({page_size, page, sort, search}) {
    return Ember.RSVP.hash({
      users: this.store.query("user", {
        filter: search,
        page_size: page_size,
        page: page,
        sort: sort
      })
    });
  },

  setupController(controller, model) {
    this._super(controller, model);
    controller.setProperties(model);
    controller.setProperties({
      page_size: model.users.get("meta.page_size"),
      page: model.users.get("meta.page")
    });
  }
});
