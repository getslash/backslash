import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('error-box', 'Integration | Component | error box', {
  integration: true
});

test('it renders', function(assert) {
  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });

  this.set('error', {
      timestamp: 1472973960,
      message: 'message',
  });
  this.render(hbs`{{error-box error=error}}`);

  assert.ok(this.$().text().trim().split('(')[0].trim().startsWith('09/04/2016'));

});
