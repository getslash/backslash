import { inject as service } from "@ember/service";
import { sort, oneWay } from "@ember/object/computed";
import PaginatedFilteredController from "../../controllers/paginated_filtered_controller";
import StatusFilterableController from "../../mixins/status-filterable/controller";

import config from "../../config/environment";
import SearchController from "../../mixins/search-controller";

export default PaginatedFilteredController.extend(
  StatusFilterableController,
  SearchController,
  {
    queryParams: ["show_planned", "search", "sort"],
    show_planned: false,
    collection: oneWay("tests"),
    sort: "test_index",
    sort_options: ["start_time", "test_index"],
    compact_view: false,

    available_page_sizes: config.APP.available_page_sizes,

    display: service(),
  }
);
