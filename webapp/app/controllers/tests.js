import Ember from 'ember';

export default Ember.ArrayController.extend({
  sortProperties: ['nId'],
  sortAscending: false,
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
