import Mixin from '@ember/object/mixin';

export default Mixin.create({
  queryParams: {
    page: {
      refreshModel: true
    },
    page_size: {
      refreshModel: true
    },
    filter: {
      refreshModel: true
    },
    show_successful: {
      refreshModel: true
    },
    show_unsuccessful: {
      refreshModel: true
    },
    show_abandoned: {
      refreshModel: true
    },
    show_skipped: {
      refreshModel: true
    }
  },

  transfer_filter_params(from_params, to_params) {
    let returned = to_params;
    if (to_params === undefined) {
      returned = {};
    }

    let query_params = this.get("queryParams");
    for (let key in query_params) {
      if (key.startsWith("show_")) {
        returned[key] = from_params[key];
      }
    }
    return returned;
  }
});
