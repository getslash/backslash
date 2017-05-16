import Ember from "ember";

export default Ember.Component.extend({
  classNames: ["error", "box"],

  classNameBindings: ["expanded"],

  expanded: false,

  actions: {
    toggle_expanded() {
      this.toggleProperty("expanded");
    }
  }
});
