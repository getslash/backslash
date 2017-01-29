import Ember from 'ember';
import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('comment-box', 'Integration | Component | comment box', {
  integration: true
});

test('it renders', function(assert) {

  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });

    let comment = 'some comment here';
    this.set('comment', Ember.Object.create({comment: comment, timestamp: 1234567}));


    this.render(hbs`{{comment-box comment=comment}}`);

    assert.ok(this.$().text().trim().startsWith('commented '));
    assert.notEqual(this.$().text().trim().indexOf(comment), -1);

});
