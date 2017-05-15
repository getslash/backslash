import Ember from "ember";

export default Ember.Mixin.create({
  jump_to_relative(offset) {
    let self = this;
    let test = self.get("model.test_model");
    let session = self.get("model.session_model");

    console.assert(test); // eslint-disable-line no-console
    console.assert(session); // eslint-disable-line no-console

    self.store
      .queryRecord("test", {
        session_id: test.get("session_id"),
        test_index: test.get("test_index") + offset
      })
      .then(function(test) {
        self.transitionToRoute(
          "session.test",
          session.get("display_id"),
          test.get("display_id")
        );
      });
  }
});
