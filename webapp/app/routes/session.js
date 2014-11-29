import Ember from 'ember';

export default Ember.Route.extend({
  model: function(params) {
    return Ember.RSVP.hash({
      session: this.get('store').find('session', params.session_id),
      tests: this.get('store').find('test', {
        session_id: params.session_id
      })
    });
  },

  setupController: function(controller, model) {
    controller.set('model', model.session);
    var testsController = this.controllerFor('tests');
    testsController.set('model', model.tests);
  }
});
