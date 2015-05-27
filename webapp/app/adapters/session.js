import Ember from 'ember';
import ApplicationAdapter from './application';

export default ApplicationAdapter.extend({
    updateRecord: function(store, type, snapshot) {
      var data = this.serialize(snapshot, { includeId: true });
      var post_data = 'id=' + data.id + '&status='+ data.edited_status;
      var url = 'api/edit_session_status';
      return new Ember.RSVP.Promise(function(resolve, reject) {
        Ember.$.ajax({
          type: 'POST',
          url: url,
          dataType: 'json',
          data: post_data
        }).then(function(data) {
          Ember.run(null, resolve, data);
        }, function(jqXHR) {
          jqXHR.then = null; // tame jQuery's ill mannered promises
          Ember.run(null, reject, jqXHR);
        });
      });
    }
});
