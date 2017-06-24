import { moduleForModel, test } from 'ember-qunit';

moduleForModel('related-entity', 'Unit | Model | related entity', {
  // Specify the other units that are required for this test.
  needs: []
});

test('it exists', function(assert) {
  let model = this.subject();
  // let store = this.store();
  assert.ok(!!model);
});
