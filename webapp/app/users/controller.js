import Controller from "@ember/controller";
import config from "../config/environment";

import SearchController from "../mixins/search-controller";

export default Controller.extend(SearchController, {
  queryParams: ["sort", "page", "page_size", "search"],

  page: 1,
  page_size: config.APP.default_page_size,

  sort: "last_activity",

  sort_options: [
    "last_activity",
    "first_name,last_name",
    "last_name,first_name",
  ],
});
