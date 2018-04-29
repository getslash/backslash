import EmberObject from '@ember/object';
import Service, { inject as service } from '@ember/service';

export default Service.extend({
  api: service(),

  init() {
    this.set("_cache", EmberObject.create());
  },

  get_all() {
    let self = this;
    return this.get("api").call("get_app_config").then(function(r) {
      for (let attr in r.result) {
        if (r.result.hasOwnProperty(attr)) {
          self.set(`_cache.${attr}`, r.result[attr]);
        }
      }
      return r.result;
    });
  },

  get_cached(name) {
    return this.get(`_cache.${name}`);
  }
});
