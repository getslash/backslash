import { reject, hash } from 'rsvp';
import Route from '@ember/routing/route';

export default Route.extend({
  model({test_id}) {
    let self = this;
    return self.store.query("test", {id: test_id}).then(function(tests) {
      let test = tests.get('firstObject');
      if (!test) {
        return reject({not_found: true});
      }
      return hash({
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
