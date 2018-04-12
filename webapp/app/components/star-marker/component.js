import Component from '@ember/component';

export default Component.extend({
  is_starred: false,
  actions: {
    toggle: function() {
      this.sendAction('toggle');
    },
  },
});
