import { inject as service } from '@ember/service';
import Helper from '@ember/component/helper';

export default Helper.extend({
  runtime_config: service(),

  compute(params /*, hash*/) {
    let cached = this.get("runtime_config").get_cached(
      `display_names.${params[0]}`
    );
    return cached;
  }
});
