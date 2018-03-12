import { alias } from '@ember/object/computed';
import Component from '@ember/component';

export default Component.extend({
  classNames: ["query-item"],
  user: alias('item'),
});
