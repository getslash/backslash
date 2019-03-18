import { Promise as EmberPromise } from "rsvp";
import EmberObject from "@ember/object";
import Service, { inject as service } from "@ember/service";

export default Service.extend({
  api: service(),

  init() {
    this._super(...arguments);
    this.set("_cache", EmberObject.create());
  },

  _cache_populated: false,

  ensure_cache_populated() {
    if (!this.get("_cache_populated")) {
      return this.get_all();
    }
  },

  get_all() {
    let self = this;
    return this.get("api")
      .call("get_preferences")
      .then(function(r) {
        for (let attr in r.result) {
          if (r.result.hasOwnProperty(attr)) {
            self.set(`_cache.${attr}`, r.result[attr]);
            self.set(attr, r.result[attr]);
            self.set("_cache_populated", true);
          }
        }
        return r.result;
      });
  },

  set_pref(name, value) {
    let self = this;
    return this.get("api")
      .call("set_preference", { preference: name, value: value })
      .then(function(result) {
        self.set(name, result.result);
        return result.result;
      });
  },

  get_cached(name) {
    const cache_attr = `_cache.${name}`;
    return this.get(cache_attr);
  },

  get_pref(name) {
    let self = this;
    let returned = this.get_cached(name);

    if (returned === undefined) {
      return self.get_all().then(function(prefs) {
        self.set("_cache", prefs);
        return prefs[name];
      });
    }

    return new EmberPromise(function(resolve) {
      resolve(returned);
    });
  },
});
