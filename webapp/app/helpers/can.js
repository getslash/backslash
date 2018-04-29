import { inject as service } from '@ember/service';
import Helper from '@ember/component/helper';

export default Helper.extend({
  session: service(),

  compute(params) {
    return this.get(
      "session.data.authenticated.current_user.capabilities." + params[0]
    );
  }
});
