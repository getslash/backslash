import Ember from "ember";

export default Ember.Component.extend({
  results: null,
  meta: null,
  show_subjects: true,
  show_users: true,
  session_model: null,

  display: Ember.inject.service(),

  filter_config: Ember.computed.oneWay("results.meta.filter_config"),

  actions: {
    set_page_size(size) {
      this.set("page_size", size);
    }
  }
});
