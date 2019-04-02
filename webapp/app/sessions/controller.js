import { inject as service } from "@ember/service";
import { oneWay } from "@ember/object/computed";
import Controller from "@ember/controller";

import StatusFilterableController from "./../mixins/status-filterable/controller";
import config from "../config/environment";
import SearchController from "../mixins/search-controller";

export default Controller.extend(StatusFilterableController, SearchController, {
  // default pagination parameters
  page: 1,
  page_size: config.APP.default_page_size,

  collection: oneWay("sessions"),

  api: service(),
  display: service(),

  queryParams: ["search", "page", "page_size"],

  actions: {
    async discard_results() {
      if (
        !window.confirm(
          "This will mark all search results for future deletion. Are you sure?"
        )
      ) {
        return;
      }
      await this.get("api").call("discard_sessions_search", {
        search_string: this.get("search"),
      });
    },
  },
});
