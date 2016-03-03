import Ember from 'ember';

export default Ember.Helper.extend({
  session: Ember.inject.service(),

  compute(params) {
      return true;
  }
});
