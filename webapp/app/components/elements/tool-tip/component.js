//components/my-button.js
import TooltipsterComponent
  from "ember-cli-tooltipster/components/tool-tipster";

export default TooltipsterComponent.extend({
  tagName: "span",
  theme: "tooltipster-borderless",
  distance: 1
});
