import { inject as service } from "@ember/service";
import config from "../../config/environment";
import { notEmpty, gt } from "@ember/object/computed";
import { computed } from "@ember/object";
import Component from "@ember/component";

export default Component.extend({
  display: service(),

  classNames: "d-flex mt-1",
  sort_options: null,
  available_page_sizes: config.APP.available_page_sizes,
  page: 1,
  has_next: false,
  num_pages: null,
  show_settings: true,
  filter_controller: null,
  compact_view: null,

  has_last: notEmpty("num_pages"),
  has_prev: gt("page", 1),

  normalized_sort_options: computed("sort_options", function() {
    let options = this.get("sort_options");
    if (!options) {
      return null;
    }
    let returned = [];

    for (let option of options) {
      returned.push({
        option: option,
        display: option
          .split(",")
          .map(part => part.replace("_", " "))
          .join(", "),
      });
    }
    return returned;
  }),

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
