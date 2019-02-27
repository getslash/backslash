import config from "../../config/environment";
import { notEmpty, gt } from "@ember/object/computed";
import { computed } from "@ember/object";
import Component from "@ember/component";

export default Component.extend({
  classNames: "d-flex mt-1",

  available_page_sizes: config.APP.available_page_sizes,
  page: 1,
  has_next: false,
  num_pages: null,

  filter_controller: null,

  has_last: notEmpty("num_pages"),
  has_prev: gt("page", 1),

  filters: computed(function() {
    let returned = [
      { name: "successful" },
      { name: "unsuccessful" },
      { name: "skipped" },
      { name: "abandoned" },
      { name: "planned" },
    ];

    for (let filter of returned) {
      filter.attr = `show_${filter.name}`;
    }
    return returned;
  }),

  actions: {
    first_page() {
      this.set("page", 1);
    },

    next_page() {
      this.incrementProperty("page");
    },

    prev_page() {
      this.decrementProperty("page");
    },

    last_page() {
      this.set("page", this.get("num_pages"));
    },
  },
});
