import Ember from "ember";

export default Ember.Route.extend({
  model({test_id}) {
    let self = this;
    return self.store.query("test", {id: test_id}).then(function(tests) {
      let test = tests.get('firstObject');
      if (!test) {
        return Ember.RSVP.reject({not_found: true});
      }
      return Ember.RSVP.hash({
        test: test,
        session: self.store.find("session", test.get("session_id"))
      });
    });
  },

  afterModel(model) {
    this.replaceWith(
      "session.test",
      model.session.get("display_id"),
      model.test.get("display_id")
    );
  }
});
