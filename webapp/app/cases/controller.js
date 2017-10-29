import Ember from "ember";
import config from "../config/environment";
import SearchControllerMixin from "./../mixins/search-controller";

export default Ember.Controller.extend(SearchControllerMixin, {
  queryParams: ["search", "page", "page_size"],

  page: 1,
  available_page_sizes: config.APP.available_page_sizes,
  page_size: config.APP.default_page_size,
  searching: false,

});
