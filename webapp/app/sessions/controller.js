import Ember from "ember";

import config from "../config/environment";
import StatusFilterableController
  from "./../mixins/status-filterable/controller";
import SearchController from "../mixins/search-controller";

export default Ember.Controller.extend(StatusFilterableController, SearchController, {
  available_page_sizes: config.APP.available_page_sizes,
  page_size: config.APP.default_page_size,

  collection: Ember.computed.oneWay("sessions"),

  api: Ember.inject.service(),
  display: Ember.inject.service(),

  queryParams: ["search", "page", "page_size"],

  actions: {

    async discard_results() {
      if (!window.confirm("This will mark all search results for future deletion. Are you sure?")) {
        return;
      }
      await this.get('api').call('discard_sessions_search', {
        search_string: this.get('search')
      });
    },
  },


});
