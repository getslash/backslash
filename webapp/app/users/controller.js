import Ember from "ember";
import config from "../config/environment";

import SearchController from "../mixins/search-controller";

export default Ember.Controller.extend(SearchController, {
  queryParams: ["sort", "page", "page_size", "search"],

  available_page_sizes: config.APP.available_page_sizes,
  page_size: config.APP.default_page_size,

  sort: "last_activity",

  sort_options: ["last_activity", "first_name", "last_name"]
});
