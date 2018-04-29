import Component from '@ember/component';

export default Component.extend({

  expanded: false,

  classNames: ['text-center'],
  classNameBindings: ['expanded'],

  click() {
    this.toggleProperty('expanded');
  },
});
