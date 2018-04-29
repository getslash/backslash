import { hash } from 'rsvp';
import Route from '@ember/routing/route';

import PaginatedRoute from "../mixins/paginated-route";
import ComplexModelRoute from "../mixins/complex-model-route";
import SearchRouteMixin from "../mixins/search-route";
import AuthenticatedRouteMixin
  from "ember-simple-auth/mixins/authenticated-route-mixin";


export default Route.extend(
  PaginatedRoute, AuthenticatedRouteMixin,
  ComplexModelRoute, SearchRouteMixin, {


  queryParams: {
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

    return hash({
      search: search,
      cases: this.store.query('case', query),
    }).catch(function(exception) {
      return {error: exception.errors.get('firstObject')};
    });
  },

});
