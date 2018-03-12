import { inject as service } from '@ember/service';
import { sort, oneWay } from '@ember/object/computed';
import PaginatedFilteredController
  from "../../controllers/paginated_filtered_controller";
import StatusFilterableController
  from "../../mixins/status-filterable/controller";

import config from "../../config/environment";

export default PaginatedFilteredController.extend(StatusFilterableController, {
  queryParams: ["show_planned"],
  show_planned: false,
  sortProperties: ['test_index:desc'],
  sortedTests: sort('tests', 'sortProperties'),
  collection: oneWay("tests"),

  available_page_sizes: config.APP.available_page_sizes,

  display: service()
});
