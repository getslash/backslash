import Ember from "ember";

export default Ember.Mixin.create({
  actions: {
    refreshRoute: function() {
      this.refresh();
    }
  }
});
