import Controller from '@ember/controller';

export default Controller.extend({
  additional_metadata: function() {
    return { "Ran from": this.get("session_model.hostname") };
  }.property("session_model.hostname")
});
