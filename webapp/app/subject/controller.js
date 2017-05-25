import Ember from "ember";

import PaginatedFilteredController
  from "../controllers/paginated_filtered_controller";
import StatusFilterableController from "../mixins/status-filterable/controller";

import config from "../config/environment";

export default PaginatedFilteredController.extend(StatusFilterableController, {
  queryParms: ["page", "page_size"],

  collection: Ember.computed.oneWay("sessions"),

  display: Ember.inject.service(),

  available_page_sizes: config.APP.available_page_sizes,
  page_size: config.APP.default_page_size
});
