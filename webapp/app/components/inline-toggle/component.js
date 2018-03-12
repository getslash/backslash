import Component from '@ember/component';

export default Component.extend({
  tagName: "span",

  classNames: ["clickable"],
  classNameBindings: ["value:enabled"],
  value: false,

  click() {
    this.toggleProperty("value");
    return false;
  }
});
