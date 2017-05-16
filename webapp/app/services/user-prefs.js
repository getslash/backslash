import Ember from "ember";

export default Ember.Service.extend({
  api: Ember.inject.service(),

  init() {
    this.set("_cache", Ember.Object.create());
  },

  _cache_populated: false,

  ensure_cache_populated() {
    if (!this.get("_cache_populated")) {
      return this.get_all();
    }
  },

  get_all() {
    let self = this;
    return this.get("api").call("get_preferences").then(function(r) {
      for (let attr in r.result) {
        if (r.result.hasOwnProperty(attr)) {
          self.set(`_cache.${attr}`, r.result[attr]);
          self.set("_cache_populated", true);
        }
      }
      return r.result;
    });
  },

  set_pref(name, value) {
    return this.get("api")
      .call("set_preference", { preference: name, value: value })
      .then(function(result) {
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

    return new Ember.RSVP.Promise(function(resolve) {
      resolve(returned);
    });
  }
});
