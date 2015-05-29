import Ember from 'ember';
import DurationMixinMixin from '../../../mixins/duration-mixin';
import { module, test } from 'qunit';

module('Unit | Mixin | duration mixin');

// Replace this with your real tests.
test('duration works', function(assert) {
    var DurationMixinObject = Ember.Object.extend(DurationMixinMixin, {
        start_time: '2013-02-08 09:30:26',
        end_time: '2013-02-08 09:41:00'
    });
    var subject = DurationMixinObject.create();
    assert.ok(subject);

    assert.equal(subject.get('humanizedDuration'), '11 minutes');
    assert.equal(subject.get('durationSeconds'), 634);


});
