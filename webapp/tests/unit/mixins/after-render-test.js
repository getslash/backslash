import Ember from 'ember';
import AfterRenderMixin from '../../../mixins/after-render';
import { module, test } from 'qunit';

module('AfterRenderMixin');

// Replace this with your real tests.
test('it works', function(assert) {
  var AfterRenderObject = Ember.Object.extend(AfterRenderMixin);
  var subject = AfterRenderObject.create();
  assert.assert.ok(subject);
});
