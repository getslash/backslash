import { moduleFor, test } from 'ember-qunit';

moduleFor('service:runtime-config', 'Unit | Service | runtime config', {
  // Specify the other units that are required for this test.
  needs: ['service:api']
});

// Replace this with your real tests.
test('it exists', function(assert) {
  let service = this.subject();
  assert.ok(service);
});
