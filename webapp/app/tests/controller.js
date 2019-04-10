import { inject as service } from "@ember/service";
import Controller from "@ember/controller";
import config from "../config/environment";
import StatusFilterableController from "./../mixins/status-filterable/controller";
import SearchControllerMixin from "./../mixins/search-controller";

export default Controller.extend(
  StatusFilterableController,
  SearchControllerMixin,
  {
    queryParams: ["search", "page", "page_size"],

    page: 1,
    available_page_sizes: config.APP.available_page_sizes,
    page_size: config.APP.default_page_size,
    compact_view: false,
    display: service(),
  }
);
