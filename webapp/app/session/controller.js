import Ember from "ember";

export default Ember.Controller.extend({
  current_test: null,
  test_filters: null,

  display: Ember.inject.service(),
  api: Ember.inject.service(),

  actions: {
    async discard() {
      await this.get('api').call('discard_session', {session_id: parseInt(this.get('session_model.id'))});
      await this.get('session_model').reload();
    },

    async preserve() {
      await this.get('api').call('preserve_session', {session_id: parseInt(this.get('session_model.id'))});
      await this.get('session_model').reload();
    },
  },
});
