import Ember from 'ember';

export default Ember.Mixin.create({

  search: "",
  searching: true,

  clear_search() {
    this.set("search", "");
  },

  clear_page: Ember.observer('search', function() {
    this.set('page', 1);
  }),
});
