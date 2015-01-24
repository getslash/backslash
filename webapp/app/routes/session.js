import Ember from 'ember';
import RouteMixin from 'ember-cli-pagination/remote/route-mixin';

export default Ember.Route.extend(RouteMixin, {
  model: function(params) {
    params.paramMapping = {page: "page",
      perPage: "page_size",
      total_pages: "total_num_pages"};
    return Ember.RSVP.hash({
      session: this.get('store').find('session', params.session_id),
      tests: this.findPaged('test',params)
    });
  },

  setupController: function(controller, model) {
    controller.set('model', model.session);
    var testsController = this.controllerFor('tests');
    testsController.set('model', model.tests);
  }
});
