import Ember from "ember";
import config from "../config/environment";

export default Ember.Controller.extend({
  queryParams: ["sort", "page", "page_size"],

  available_page_sizes: config.APP.available_page_sizes,
  page_size: config.APP.default_page_size,

  sort: "last_activity",

  sort_options: ["last_activity", "first_name", "last_name"]
});
