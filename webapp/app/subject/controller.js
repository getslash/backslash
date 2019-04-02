import { inject as service } from '@ember/service';
import { oneWay } from '@ember/object/computed';

import PaginatedFilteredController
  from "../controllers/paginated_filtered_controller";
import StatusFilterableController from "../mixins/status-filterable/controller";

export default PaginatedFilteredController.extend(StatusFilterableController, {
  queryParms: ["page", "page_size"],

  collection: oneWay("sessions"),

  display: service(),
});
