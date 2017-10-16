import Ember from 'ember';

export default Ember.Mixin.create({

  setupController(controller) {
    this._super(...arguments);
    controller.set('searching', false);
  },

});
