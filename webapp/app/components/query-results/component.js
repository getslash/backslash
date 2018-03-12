import { oneWay } from '@ember/object/computed';
import { inject as service } from '@ember/service';
import Component from '@ember/component';

export default Component.extend({
  results: null,
  meta: null,
  show_subjects: true,
  show_users: true,
  session_model: null,

  display: service(),

  filter_config: oneWay("results.meta.filter_config"),

  actions: {
    set_page_size(size) {
      this.set("page_size", size);
    }
  }
});
