import Ember from 'ember';
import RefreshableRouteMixin from '../../../mixins/refreshable-route';
import { module, test } from 'qunit';

module('Unit | Mixin | refreshable route');

// Replace this with your real tests.
test('it works', function(assert) {
  var RefreshableRouteObject = Ember.Object.extend(RefreshableRouteMixin);
  var subject = RefreshableRouteObject.create();
  assert.ok(subject);
});
