import Ember from 'ember';
import HasLogicalIdMixin from '../../../mixins/has-logical-id';
import { module, test } from 'qunit';

module('Unit | Mixin | has logical id');

// Replace this with your real tests.
test('it works', function(assert) {
  var HasLogicalIdObject = Ember.Object.extend(HasLogicalIdMixin);
  var subject = HasLogicalIdObject.create();
  assert.ok(subject);
});
