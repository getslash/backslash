import Ember from "ember";

export default Ember.Component.extend({
  expanded: false,

  classNameBindings: ['expanded'],

  actions: {
    toggle_expanded() {
      this.toggleProperty("expanded");
    }
  }
});
