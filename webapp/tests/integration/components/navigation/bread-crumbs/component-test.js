import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('navigation/bread-crumbs', 'Integration | Component | navigation/bread crumbs', {
  integration: true
});

test('it renders', function(assert) {
  
  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });" + EOL + EOL +

  this.render(hbs`{{navigation/bread-crumbs}}`);

  assert.equal(this.$().text().trim(), '');

  // Template block usage:" + EOL +
  this.render(hbs`
    {{#navigation/bread-crumbs}}
      template block text
    {{/navigation/bread-crumbs}}
  `);

  assert.equal(this.$().text().trim(), 'template block text');
});
