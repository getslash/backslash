import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('key-value-data', 'Integration | Component | key value data', {
  integration: true
});

test('it renders', function(assert) {
  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });

    this.set('data', {key: 'value'});
    this.render(hbs`{{key-value-data data=data}}`);

    assert.equal(this.$().find('tr td:eq(0)').text().trim(), 'key');
    assert.equal(this.$().find('tr td:eq(1)').text().trim(), 'value');
});
