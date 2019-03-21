import Component from '@ember/component';

export default Component.extend({
  tagName: "li",

  classNames: "nav-item dropdown",
  classNameBindings: ["alignment"],

  alignment: function() {
    return `navbar-${this.get('align')}`;
  }.property('align'),

  dropdown_id: function() {
    return `dropdown-${this.elementId}`;
  }.property(),

  options: null,

  align: 'right',

  actions: {
    set_value(value) {
      this.set("value", value);
    }
  }
});
