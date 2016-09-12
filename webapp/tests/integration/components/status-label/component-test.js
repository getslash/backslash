import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('status-label', 'Integration | Component | status label', {
  integration: true
});

test('it renders', function(assert) {
  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });

  this.set('status', 'success');

  this.render(hbs`{{status-label status=status}}`);

  assert.ok(this.$().find('i').hasClass('fa-check'));
});
