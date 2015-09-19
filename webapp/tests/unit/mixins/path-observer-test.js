import Ember from 'ember';
import PathObserverMixin from '../../../mixins/path-observer';
import { module, test } from 'qunit';

module('Unit | Mixin | path observer');

// Replace this with your real tests.
test('it works', function(assert) {
  var PathObserverObject = Ember.Object.extend(PathObserverMixin);
  var subject = PathObserverObject.create();
  assert.ok(subject);
});
