import Ember from "ember";

export default Ember.Component.extend({
  expanded: false,
  error: null,

  classNames: ['error-box'],
  classNameBindings: ['expanded', 'error.is_interruption:interruption'],

  actions: {
    toggle_expanded() {
      this.toggleProperty("expanded");
    }
  }
});
