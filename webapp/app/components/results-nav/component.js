import { notEmpty, gt } from '@ember/object/computed';
import Component from '@ember/component';

export default Component.extend({
  page: 1,
  has_next: false,
  num_pages: null,

  has_last: notEmpty('num_pages'),

  has_prev: gt("page", 1),

  actions: {
    first_page() {
      this.set("page", 1);
    },

    next_page() {
      this.incrementProperty("page");
    },

    prev_page() {
      this.decrementProperty("page");
    },

    last_page() {
      this.set('page', this.get('num_pages'));
    },
  }
});
