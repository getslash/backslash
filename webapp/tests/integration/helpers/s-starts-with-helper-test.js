
import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('s-starts-with-helper', 'helper:s-starts-with', {
  integration: true
});

test('positive', function(assert) {
  this.set('s', 'testme');
  this.set('prefix', 'test')

  this.render(hbs`{{s-starts-with s prefix}}`);

  assert.equal(this.$().text().trim(), 'true');
});

test('negative', function(assert) {
  this.set('s', 'testme');
  this.set('prefix', 'test1')

  this.render(hbs`{{s-starts-with s prefix}}`);

  assert.equal(this.$().text().trim(), 'false');
});

test('positive multiple', function(assert) {
    this.set('s', 'https://blap');

    this.render(hbs`{{s-starts-with s "http://" "https://"}}`);

    assert.equal(this.$().text().trim(), 'false');
});

test('negative multiple', function(assert) {
    this.set('s', 's://blap');

    this.render(hbs`{{s-starts-with s "http://" "https://"}}`);

    assert.equal(this.$().text().trim(), 'false');
});


