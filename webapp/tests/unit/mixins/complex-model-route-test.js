import Ember from 'ember';
import ComplexModelRouteMixin from 'webapp/mixins/complex-model-route';
import { module, test } from 'qunit';

module('Unit | Mixin | complex model route');

// Replace this with your real tests.
test('it works', function(assert) {
  let ComplexModelRouteObject = Ember.Object.extend(ComplexModelRouteMixin);
  let subject = ComplexModelRouteObject.create();
  assert.ok(subject);
});
