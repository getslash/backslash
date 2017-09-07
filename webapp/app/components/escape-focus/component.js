import Ember from "ember";

export default Ember.Component.extend({
  classNames: ["input-group col-xs-6"],

  classNameBindings: ['error:has-error'],

  keyUp: function(e) {
    if (e.keyCode === 27) {
      this.$("input.search-bar").blur();
    }
  }
});
