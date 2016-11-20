import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('warning-box', 'Integration | Component | warning box', {
  integration: true
});

test('it renders', function(assert) {
  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });

    this.set('warning', {timestamp: 1472973960.629628, filename: 'testme.py', lineno: 10});
    this.render(hbs`{{warning-box warning=warning}}`);

    assert.ok(this.$().text().trim().startsWith(`09/04/2016`));
});
