import Component from '@ember/component';

export default Component.extend({
  classNames: "copyable-text",
  classNameBindings: ['preformatted'],

  value: null,
  copy_value: null,

  clipboard_text: function() {
    let returned = this.get('copy_value');
    if (returned) {
      return returned;
    }
    return this.get('value');
  }.property('value', 'copy_value'),

  preformatted: false,
});
