import Ember from "ember";

export default Ember.Component.extend({
  expanded: false,

  actions: {
    toggle_expanded() {
      this.toggleProperty("expanded");
    }
  }
});
