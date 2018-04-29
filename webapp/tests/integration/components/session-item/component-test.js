import EmberObject from '@ember/object';
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

test('Session with errors has unsuccessful class', function(assert) {

    this.set('item', _normal_session());
    this.set('item.num_errors', 10);

    this.render(hbs`{{session-item item=item}}`);
    assert.ok(this.$('>:first-child').hasClass('unsuccessful'), 'does not have unsuccessful class');
});


function _normal_session() {
    return EmberObject.create({
	has_tests_left_to_run: false,
	finished_running: true,
	num_finished_tests: 10,
	total_num_tests: 10,
	start_time: 100,
	end_time: 100,
	computed_status: 'success',
	num_errors: 0,
    });
}
