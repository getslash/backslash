import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('status-icon', 'Integration | Component | status icon', {
  integration: true
});

test('status icon correct', function(assert) {
  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });

  this.set('status', 'success');
  this.render(hbs`{{status-icon status=status}}`);

  assert.ok(this.$().find('.fa').hasClass('fa-check'));

});
