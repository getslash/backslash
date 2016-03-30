import Ember from 'ember';
import {timeout, task} from 'ember-concurrency';

export default Ember.Component.extend({
    tagName: 'li',
    classNames: 'menu-toggle',

    _value: null,

    update_internal_value_from_external: function() {
        this.set('_value', this.get('toggled'));
    }.observes('toggled').on('init'),

    update_external_value_from_internal: function() {
        this.get('update').perform();
    }.observes('_value'),


    update: task(function* () {
        yield timeout(200);
        this.set('toggled', this.get('_value'));
    }).restartable(),
});
