import Ember from 'ember';

export default Ember.Route.extend({
  model: function(params) {
    return Ember.RSVP.hash({
      test: this.store.find('test', params.test_id),
      testErrors: this.store.find('testError',{test_id: params.test_id})

    });

  }
});
