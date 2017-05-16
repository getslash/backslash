import { moduleFor, test } from "ember-qunit";
import start_mirage from "../../helpers/setup-mirage";

moduleFor("service:user-prefs", "Unit | Service | user prefs", {
  needs: ["service:api"],
  beforeEach() {
    start_mirage(this.container);
  },
  afterEach() {
    window.server.shutdown();
  }
});

test("get pref cached", function(assert) {
  let value = "some value here";
  let service = this.subject();
  service.set("_cache.key", value);
  return service.get_pref("key").then(got_value => {
    assert.equal(got_value, value);
  });
});

test("get pref not cached", function(assert) {
  let service = this.subject();
  return service.get_pref("time_format").then(function(value) {
    assert.equal(value, "default_time_format");
  });
});

test("get all prefs", function(assert) {
  let service = this.subject();
  return service.get_all().then(function(value) {
    assert.deepEqual(value, {
      time_format: "default_time_format"
    });
    assert.equal(service.get("_cache.time_format"), "default_time_format");
  });
});

test("set prefs", function(assert) {
  let service = this.subject();
  const new_value = "new value here";
  return service.set_pref("time_format", new_value).then(function(v) {
    assert.equal(v, new_value);
  });
});
