import Ember from "ember";

var InfrastructureIconComponent = Ember.Component.extend({
  tagName: "span"
});

InfrastructureIconComponent.reopenClass({
  positionalParams: ["infrastructure"]
});

export default InfrastructureIconComponent;
