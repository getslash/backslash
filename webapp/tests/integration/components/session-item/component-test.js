import Ember from 'ember';
import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('session-item', 'Integration | Component | session item', {
    integration: true,
});

test('Regular session rendering', function(assert) {

    this.set('item', _normal_session());

    this.render(hbs`{{session-item item=item}}`);
    assert.ok(this.$('>:first-child').hasClass('success'), 'has success class');
});

test('Session with errors has error class', function(assert) {

    this.set('item', _normal_session());
    this.set('item.num_errors', 10);

    this.render(hbs`{{session-item item=item}}`);
    assert.notOk(this.$('>:first-child').hasClass('success'), 'has success class');
    assert.ok(this.$('>:first-child').hasClass('failed'), 'does not have failed class');
});


function _normal_session() {
    return Ember.Object.create({
	has_tests_left_to_run: false,
	finished_running: true,
	num_finished_tests: 10,
	total_num_tests: 10,
	start_time: 100,
	end_time: 100,
	status: 'success',
	num_errors: 0,
    });
}
