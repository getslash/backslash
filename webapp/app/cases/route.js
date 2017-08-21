import Ember from 'ember';

import PaginatedRoute from "../mixins/paginated-route";
import ComplexModelRoute from "../mixins/complex-model-route";
import SearchRouteMixin from "../mixins/search-route";
import AuthenticatedRouteMixin
  from "ember-simple-auth/mixins/authenticated-route-mixin";


export default Ember.Route.extend(
  PaginatedRoute, AuthenticatedRouteMixin,
  ComplexModelRoute, SearchRouteMixin, {


  queryParams: {
    filter: {
      replace: true,
      refreshModel: true
    },
    page: {
      refreshModel: true
    },
    page_size: {
      refreshModel: true
    },
    search: {
      refreshModel: true,
    },
  },

  model({search, page, page_size}) {
    let query = { page: page, page_size: page_size, search: search};

    return Ember.RSVP.hash({
      search: search,
      cases: this.store.query('case', query),
    });
  },

});
