import Ember from 'ember';

export default Ember.ArrayController.extend({
  sortProperties: ['integerId'],
  sortAscending: false,

  queryParams: ["page","perPage"],
  page: 1,
  perPage: 10,
  perPageChanged: function(){
    this.set('page', 1);
  }.observes('perPage'),

  pageBinding: "content.page",
  perPageBinding: "content.perPage",
  totalPagesBinding: "content.totalPages",

  resultsPerPage: [10, 20, 50, 100],

  actions: {
    sortBy: function(property) {
      this.set('sortProperties', [property]);
      this.set('sortAscending', !this.get('sortAscending'));
      Ember.$("#tests-header").children().removeClass('headerSortDown');
      Ember.$("#tests-header").children().removeClass('headerSortUp');
      var header_name = "#header-" + property;
      if (this.get('sortAscending'))
      {
        Ember.$(header_name).addClass('headerSortDown');
      }
      else
      {
        Ember.$(header_name).addClass('headerSortUp');
      }
    }

  }
});
