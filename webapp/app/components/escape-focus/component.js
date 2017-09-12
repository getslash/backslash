import Ember from "ember";

export default Ember.Component.extend({
  classNames: ["input-group"],

  classNameBindings: ['error:has-error'],

  keyUp: function(e) {
    if (e.keyCode === 27) {
      this.$("input.search-bar").blur();
    }
  }
});
