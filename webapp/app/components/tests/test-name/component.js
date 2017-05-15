import Ember from "ember";

export default Ember.Component.extend({
  tagName: "span",
  classNames: ["test-name"],

  display_params: function() {
    let params = this.get("parameters");
    if (!params) {
      return this.get("variation");
    }

    let returned = Ember.assign({}, this.get("variation"), params);
    return returned;
  }.property("parameters", "variation")
});
