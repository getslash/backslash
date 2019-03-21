import PaginatedFilteredRoute from "../routes/paginated_filtered_route";
import ComplexModelRoute from "../mixins/complex-model-route";
import AuthenticatedRouteMixin
  from "ember-simple-auth/mixins/authenticated-route-mixin";
import StatusFilterableRoute from "./../mixins/status-filterable/route";
import SearchRouteMixin from "./../mixins/search-route";

export default PaginatedFilteredRoute.extend(AuthenticatedRouteMixin, ComplexModelRoute, StatusFilterableRoute, SearchRouteMixin, {
  titleToken: "Tests",

  queryParams: {
    search: {
      replace: true,
      refreshModel: true
    },
    page: {
      refreshModel: true
    },
    page_size: {
      refreshModel: true
    }
  },

  model(params) {
    let query = { page: params.page, page_size: params.page_size };
    if (!params.search) {
      return {tests: null, error: null};
    }

    query.search = params.search;

    this.transfer_filter_params(params, query);

    return this.store
      .query("test", query)
      .then(function(tests) {
        return { tests: tests, error: null, search: query.search};
      })
      .catch(function(exception) {
        return {error: exception.errors.get('firstObject')};
      });
  },

});
