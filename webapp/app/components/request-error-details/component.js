import Component from '@ember/component';
import {computed} from '@ember/object';

export default Component.extend({
  classNames: ['container'],
  error: null,

  error_string: computed('error', function() {
    return JSON.stringify(this.get('error'));
  }),
});
