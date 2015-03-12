import Ember from 'ember';

export default Ember.Component.extend({
  showOneLine: true,

  actions: {
    toggleOneLine: function () {
      this.toggleProperty('showOneLine');
    }
  }

});
