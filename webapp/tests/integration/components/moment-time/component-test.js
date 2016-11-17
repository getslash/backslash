import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('moment-time', 'Integration | Component | moment time', {
  integration: true
});

test('it renders', function(assert) {
    this.set('unix', 1472973960);

  this.render(hbs`{{moment-time unix=unix}}`);

  assert.ok(this.$().text().trim().startsWith('09/04/2016'));
});
