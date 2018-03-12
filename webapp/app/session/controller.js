import { inject as service } from '@ember/service';
import Controller from '@ember/controller';

export default Controller.extend({
  current_test: null,
  test_filters: null,

  display: service(),
  api: service(),

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
