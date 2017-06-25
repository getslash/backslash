import Ember from "ember";
import config from "../config/environment";
import StatusFilterableController
  from "./../mixins/status-filterable/controller";

export default Ember.Controller.extend(StatusFilterableController, {
  queryParams: ["search", "page", "page_size"],

  search: "",
  entered_search: Ember.computed.oneWay("search"),
  page: 1,
  available_page_sizes: config.APP.available_page_sizes,
  page_size: config.APP.default_page_size,

  actions: {
    search() {
      this.set("page", 1);
      this.set("search", this.get("entered_search"));
    }
  }
});
