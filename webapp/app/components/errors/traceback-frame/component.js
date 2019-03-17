import { notEmpty } from "@ember/object/computed";
import { computed } from "@ember/object";
import Component from "@ember/component";
import _ from "lodash";

export default Component.extend({
  frame: null,

  classNames: ["traceback-frame"],
  classNameBindings: ["expanded", "frame.is_in_test_code:test-code"],

  variables: computed("frame.{locals,globals}", function() {
    let locals = this._sort("frame.locals");
    let globals = this._sort("frame.globals");
    return locals.concat(globals);
  }),

  _sort(attr_name) {
    let returned = [];
    let locals = this.get(attr_name) || [];
    for (let key in locals) {
      if (locals.hasOwnProperty(key)) {
        let is_attribute = key.startsWith("self.");
        let display_name = key;
        if (is_attribute) {
          display_name = display_name.substr(5);
        }
        returned.push({
          name: key,
          display_name: display_name,
          value: locals[key],
          is_attribute: is_attribute,
        });
      }
    }

    return _.sortBy(returned, o => o.name);
  },
});
