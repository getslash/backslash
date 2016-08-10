import { sStartsWith } from 'webapp/helpers/s-starts-with';
import { module, test } from 'qunit';

module('Unit | Helper | s starts with');

test('positive', function(assert) {
  let result = sStartsWith(["testme", "test"]);
  assert.ok(result);
});

test('negative', function(assert) {
  let result = sStartsWith(["testme", "test1"]);
  assert.notOk(result);
});
