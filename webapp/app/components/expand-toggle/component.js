import Ember from 'ember';

export default Ember.Component.extend({

  expanded: false,

  classNames: ['text-center'],
  classNameBindings: ['expanded'],

  click() {
    this.toggleProperty('expanded');
  },
});
