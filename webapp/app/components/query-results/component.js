import { oneWay } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import Component from "@ember/component";

export default Component.extend({
  results: null,
  meta: null,
  show_subjects: true,
  show_users: true,
  session_model: null,
  filter_controller: null,

  display: service(),

  actions: {
    set_page_size(size) {
      this.set("page_size", size);
    },
  },
});
