import Ember from 'ember';
import CommentControllerMixin from '../../../mixins/comment-controller';
import { module, test } from 'qunit';

module('Unit | Mixin | comment controller');

// Replace this with your real tests.
test('it works', function(assert) {
  var CommentControllerObject = Ember.Object.extend(CommentControllerMixin);
  var subject = CommentControllerObject.create();
  assert.ok(subject);
});
