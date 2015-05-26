import Ember from 'ember';
import RouteMixin from 'ember-cli-pagination/remote/route-mixin';

export default Ember.Route.extend(RouteMixin, {
  model: function(params) {
    params.paramMapping = {page: "page",
      perPage: "page_size",
      total_pages: "total_num_pages"};

    var paged = this.findPaged('test', params);
    paged.fromGeneralTestsTable = true;
    return paged;
  },
  actions: {
    statusChanged: function() {
      this.refresh();
    }
  }
});
