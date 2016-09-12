import { formatTestName } from 'webapp/helpers/format-test-name';
import { module, test } from 'qunit';

module('Unit | Helper | format test name');

test('without class', function(assert) {
  let result = formatTestName([{
      file_name: 'filename.py',
      class_name: null,
      name: 'name',
  }], {});
  assert.equal(result, 'filename.py:name');
});

test('with invalid class', function(assert) {
  let result = formatTestName([{
      file_name: 'filename.py',
      class_name: 'fkjdfd(',
      name: 'name',
  }], {});
  assert.equal(result, 'filename.py:name');
});


test('with class', function(assert) {
  let result = formatTestName([{
      file_name: 'filename.py',
      class_name: 'Blap',
      name: 'name',
  }], {});
  assert.equal(result, 'filename.py:Blap.name');
});

test('without filename', function(assert) {
  let result = formatTestName([{
      file_name: 'filename.py',
      class_name: 'Blap',
      name: 'name',
  }], {with_filename: false});
  assert.equal(result, 'Blap.name');
});
