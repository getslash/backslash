import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('errors/traceback-frame', 'Integration | Component | errors/traceback frame', {
  integration: true
});

test('it renders', function(assert) {
  
  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });" + EOL + EOL +

  this.render(hbs`{{errors/traceback-frame}}`);

  assert.equal(this.$().text().trim(), '');

  // Template block usage:" + EOL +
  this.render(hbs`
    {{#errors/traceback-frame}}
      template block text
    {{/errors/traceback-frame}}
  `);

  assert.equal(this.$().text().trim(), 'template block text');
});
