import Ember from 'ember';

export default Ember.Component.extend({
  classNames: ["query-item"],
  user: Ember.computed.alias('item'),
});
