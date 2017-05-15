import Ember from "ember";

export default Ember.Helper.extend({
  session: Ember.inject.service(),

  compute(params) {
    return this.get(
      "session.data.authenticated.current_user.capabilities." + params[0]
    );
  }
});
