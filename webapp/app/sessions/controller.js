import Ember from "ember";

import config from "../config/environment";
import StatusFilterableController
  from "./../mixins/status-filterable/controller";

export default Ember.Controller.extend(StatusFilterableController, {
  available_page_sizes: config.APP.available_page_sizes,
  page_size: config.APP.default_page_size,

  collection: Ember.computed.oneWay("sessions"),

  display: Ember.inject.service(),

  entered_search: Ember.computed.oneWay("search"),

  queryParams: ["search", "page", "page_size"],

  search: "",

  clear_search() {
    this.set("entered_search", "");
    this.set("search", "");
  },

  actions: {
    search() {
      this.set("page", 1);
      let entered_search = this.get("entered_search");
      this.set("search", entered_search);
    }
  }
});
