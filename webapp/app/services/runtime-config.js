import EmberObject from "@ember/object";
import Service, { inject as service } from "@ember/service";

export default Service.extend({
  api: service(),

  init() {
    this._super(...arguments);
    this.set("_cache", EmberObject.create());
  },

  async get_all() {
    let self = this;
    let response = await this.get("api").call("get_app_config");
    for (let attr in response.result) {
      if (response.result.hasOwnProperty(attr)) {
        self.set(`_cache.${attr}`, response.result[attr]);
      }
    }
    return response.result;
  },

  get_cached(name) {
    return this.get(`_cache.${name}`);
  },
});
