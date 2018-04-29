import { notEmpty } from '@ember/object/computed';
import Component from '@ember/component';
import _ from "lodash";

export default Component.extend({
  frame: null,

  classNames: ['traceback-frame'],
  classNameBindings: ['expanded', 'frame.is_in_test_code:test-code'],

  has_locals: notEmpty("frame.locals"),
  has_globals: notEmpty("frame.globals"),

  sorted_globals: function() {
    return this._sort('frame.globals');
  }.property('frame.gobals'),

  sorted_locals: function() {
    return this._sort('frame.locals');
  }.property('frame.locals'),

  _sort(attr_name) {
    let returned = [];
    let locals = this.get(attr_name) || [];
    for (let key in locals) {
      if (locals.hasOwnProperty(key)) {
        let is_attribute = key.startsWith('self.');
        let display_name = key;
        if (is_attribute) {
          display_name = display_name.substr(5);
        }
        returned.push({
          name: key,
          display_name: display_name,
          value: locals[key],
          is_attribute: is_attribute
        });
      }
    }

    return _.sortBy(returned, o => o.name);
  },

  actions: {
    click() {
      this.toggleProperty('expanded');
    },
  },
});
