import Ember from 'ember';

export default Ember.View.extend({
  didInsertElement: function() {
    Ember.$('.tree').treegrid();
    Ember.$('.tree').treegrid('collapseAll');
  },
  metaDataVisible: false,
  actions: {
    toggleMetadata: function () {
      this.toggleProperty('metaDataVisible');
    }
  }
});
