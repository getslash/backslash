import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('multi-toggle', 'Integration | Component | multi toggle', {
  integration: true
});

test('it renders', function(assert) {
  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });

    this.set('value', 'a');
    this.set('options', ['a', 'b', 'c']);

    this.render(hbs`{{multi-toggle value=value options=options}}`);

    let comp = this.$('>:first-child');
    assert.ok(comp.find('button:eq(0)').hasClass('btn-success'));
    assert.equal(comp.find('button:eq(0)').text().trim(), this.get('value').toUpperCase());
});
