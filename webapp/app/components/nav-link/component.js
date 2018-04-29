import { oneWay } from '@ember/object/computed';
import { inject as service } from '@ember/service';
import Component from '@ember/component';

export default Component.extend({
  to: null,
  tagName: "li",
  path_tracker: service(),
  current_path: oneWay("path_tracker.path"),

  classNameBindings: ["is_active:active"],

  is_active: false
});
