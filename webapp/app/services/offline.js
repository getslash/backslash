import Ember from "ember";

/* global Heyoffline */
export default Ember.Service.extend({
  service: null,

  init() {
    this.set("service", new Heyoffline());
  }
});
