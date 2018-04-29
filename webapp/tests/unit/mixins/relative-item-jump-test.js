import EmberObject from '@ember/object';
import RelativeItemJumpMixin from 'webapp/mixins/relative-item-jump';
import { module, test } from 'qunit';

module('Unit | Mixin | relative item jump');

// Replace this with your real tests.
test('it works', function(assert) {
  let RelativeItemJumpObject = EmberObject.extend(RelativeItemJumpMixin);
  let subject = RelativeItemJumpObject.create();
  assert.ok(subject);
});
