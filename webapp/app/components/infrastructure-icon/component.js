import Component from '@ember/component';

var InfrastructureIconComponent = Component.extend({
  tagName: "span"
});

InfrastructureIconComponent.reopenClass({
  positionalParams: ["infrastructure"]
});

export default InfrastructureIconComponent;
