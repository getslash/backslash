import Ember from 'ember';
import RouteMixin from 'ember-cli-pagination/remote/route-mixin';

export default Ember.Route.extend(RouteMixin, {
  model: function(params) {
    params.paramMapping = {page: "page",
      perPage: "page_size",
      total_pages: "total_num_pages"};
    return Ember.RSVP.hash({
      session: this.get('store').find('session', params.session_id),
      tests: this.findPaged('test',params),
      sessionErrors: this.store.find('error',{session_id: params.session_id})

    });
  },

  setupController: function(controller, model) {
    controller.set('model', model.session);
    controller.set('model.sessionErrors', model.sessionErrors);

    //for the rendering
    model.tests.fromGeneralTestsTable = false;

    var testsController = this.controllerFor('tests');
    testsController.set('model', model.tests);

  },
  actions: {
    statusChanged: function() {
      this.refresh();
    }
  }
});
