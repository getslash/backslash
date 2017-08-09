import Ember from 'ember';

export default Ember.Mixin.create({
  page: 1,
  page_size: 25,

  queryParams: [
    "page",
    "page_size",
  ],

});
