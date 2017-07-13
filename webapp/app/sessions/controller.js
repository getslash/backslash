import Ember from "ember";

import config from "../config/environment";
import StatusFilterableController
  from "./../mixins/status-filterable/controller";
import SearchController from "../mixins/search-controller";

export default Ember.Controller.extend(StatusFilterableController, SearchController, {
  available_page_sizes: config.APP.available_page_sizes,
  page_size: config.APP.default_page_size,

  collection: Ember.computed.oneWay("sessions"),

  display: Ember.inject.service(),

  queryParams: ["search", "page", "page_size"],


});
