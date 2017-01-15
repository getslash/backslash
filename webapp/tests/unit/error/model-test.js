import Ember from 'ember';
import { moduleForModel, test } from 'ember-qunit';

moduleForModel('error', 'Unit | Model | error', {
  // Specify the other units that are required for this test.
  needs: []
});


test('long message, no newlines', function(assert) {
    let model = this.subject();
    const msg = 'short msg here'.repeat(600);
    Ember.run(function() {
        model.set('message', msg);
    });
    assert.equal(model.get('full_message'), msg);
    assert.notEqual(model.get('abbreviated_message'), msg);
    assert.ok(model.get('abbreviated_message').endsWith('...'));
});


test('long message, with newlines', function(assert) {
    let model = this.subject();
    const msg = 'short msg here\n'.repeat(600);
    Ember.run(function() {
        model.set('message', msg);
    });
    assert.equal(model.get('full_message'), msg);
    assert.notEqual(model.get('abbreviated_message'), msg);
    assert.ok(model.get('abbreviated_message').endsWith('...'));
});


test('short message', function(assert) {
    let model = this.subject();
    const msg = 'short msg here';
    Ember.run(function() {
        model.set('message', msg);
    });
    assert.equal(model.get('full_message'), msg);
    assert.equal(model.get('abbreviated_message'), msg);
});
