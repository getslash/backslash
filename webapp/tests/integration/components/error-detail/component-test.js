import EmberObject from '@ember/object';
import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('error-detail', 'Integration | Component | error detail', {
  integration: true
});

test('it renders', function(assert) {
  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });
    let exception_type = 'SomeError';
    this.set('error', EmberObject.create({exception_type: exception_type}));

    this.render(hbs`{{error-detail error=error}}`);
    let component = this.$('>:first-child');

    assert.equal(component.find('table td:eq(1)').text(), exception_type);
});
