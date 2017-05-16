import Ember from "ember";

export default Ember.Component.extend({
  actions: {
    back: function() {
      window.history.back();
    }
  }
});
