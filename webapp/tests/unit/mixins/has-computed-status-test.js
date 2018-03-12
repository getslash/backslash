import EmberObject from '@ember/object';
import HasComputedStatusMixin from 'webapp/mixins/has-computed-status';
import { module, test } from 'qunit';

module('Unit | Mixin | has computed status');

// Replace this with your real tests.
test('it works', function(assert) {
  let HasComputedStatusObject = EmberObject.extend(HasComputedStatusMixin);
  let subject = HasComputedStatusObject.create();
  assert.ok(subject);
});
