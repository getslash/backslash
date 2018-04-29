import Component from '@ember/component';

export default Component.extend({
  classNames: ["input-group"],

  classNameBindings: ['error:has-error'],

  keyUp: function(e) {
    if (e.keyCode === 27) {
      this.$("input.search-bar").blur();
    }
  }
});
