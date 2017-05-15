import { moduleFor, test } from 'ember-qunit';

moduleFor('route:user/preferences', 'Unit | Route | user/preferences', {
  // Specify the other units that are required for this test.
  needs: ['service:session', 'service:user_prefs']
});

test('it exists', function(assert) {
  let route = this.subject();
  assert.ok(route);
});
