import Controller from '@ember/controller';

import config from "../config/environment";

export default Controller.extend({
  available_page_sizes: config.APP.available_page_sizes,
  page: 1,
  page_size: config.APP.default_page_size,

  queryParams: ["sort", "page", "page_size"],

  sort: "last_activity",

  sort_options: ["last_activity", "name"]
});
