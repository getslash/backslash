import Ember from 'ember';

export default Ember.Route.extend({
    model: function(params) {
      return this.store.findQuery('session', params.filters);
    }/*,
    controllerName: 'sessions',

    renderTemplate: function() {
      this.render('sessions');


    }
    ,

    setupController: function(controller,model) {
      controller.set('model', model);
    }*/
  });
