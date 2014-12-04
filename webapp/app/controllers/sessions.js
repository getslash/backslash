import Ember from 'ember';

export default Ember.ArrayController.extend({
  showRunning: false,

  filteredSessions: function() {
    var sessions = this.get('model');

    if (!sessions || !this.get('showRunning')) {
      return sessions;
    }

    return sessions.filter(function(item) {
      return item.get('isRunning');
    });
  }.property('showRunning')
});
