import { humanizeDuration } from 'webapp/helpers/humanize-duration';
import { module, test } from 'qunit';

module('Unit | Helper | humanize duration');

// Replace this with your real tests.
test('basic', function(assert) {
  let result = humanizeDuration([], {
      start: 1471356210.64401,
      end: 1471359153.16362,
  });
  assert.equal(result, '49m 2s');
});
