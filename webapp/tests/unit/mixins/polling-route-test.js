import Ember from 'ember';
import PollingRouteMixin from '../../../mixins/polling-route';
import { module, test } from 'qunit';

module('Unit | Mixin | polling route');

// Replace this with your real tests.
test('it works', function(assert) {
  var PollingRouteObject = Ember.Object.extend(PollingRouteMixin);
  var subject = PollingRouteObject.create();
  assert.ok(subject);
});
