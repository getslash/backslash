import { moduleFor, test } from 'ember-qunit';

moduleFor('route:session/info', 'Unit | Route | session/info', {
  // Specify the other units that are required for this test.
  needs: ['service:api']
});

test('it exists', function(assert) {
  let route = this.subject();
  assert.ok(route);
});
