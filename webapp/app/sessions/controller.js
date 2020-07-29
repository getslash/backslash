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
  compact_view: null,
  api: service(),
  display: service(),

  queryParams: ["search", "page", "page_size"],

  actions: {
    async discard_results() {
      var days = parseInt(prompt("This will mark all search results for future deletion."
        + "\n" + "Please provide number of days to keep sessions"), 10);
      if (Number.isInteger(days))
      {
        await this.get("api").call("discard_sessions_search", {
          search_string: this.get("search"),
          grace_period_seconds: days * 60 * 60 * 24
        });
      }
    },
  },
});
