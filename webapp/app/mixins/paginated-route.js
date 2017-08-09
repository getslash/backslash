import Ember from 'ember';

export default Ember.Mixin.create({
  queryParams: {
    page: {
      refreshModel: true
    },
    page_size: {
      refreshModel: true
    },
  },

});
