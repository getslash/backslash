import Ember from 'ember';

export default Ember.Controller.extend({
  actions: {
    close: function() {
      this.set('selectedStatus', this.get('model.editedStatus'));
      this.send('statusChanged'); //to reset the whole thing from server (called in both save and close)
      return this.send('closeModal');
    },
    save: function() {
      this.set('model.editedStatus', this.get('selectedStatus'));
      this.get('model').save();
    }
  },
  sessionStatuses: ['', 'SUCCESS', 'FAILURE', 'RUNNING'],
  selectedStatus: ""
});
