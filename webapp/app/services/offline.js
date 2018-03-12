import Service from '@ember/service';

/* global Heyoffline */
export default Service.extend({
  service: null,

  init() {
    this.set("service", new Heyoffline());
  }
});
