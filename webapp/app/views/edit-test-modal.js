import Ember from 'ember';

export default Ember.View.extend({
  didInsertElement : function(){
    //we have no model, bu controller has one...
    this.get('controller').set('selectedStatus', this.get('controller').get(('model.editedStatus')));
  }
});
