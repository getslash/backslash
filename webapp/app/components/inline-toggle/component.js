import Ember from 'ember';

export default Ember.Component.extend({
    tagName: 'span',

    classNames: ['clickable'],
    classNameBindings: ['value:enabled'],
    value: false,

    click() {
        this.toggleProperty('value');
        return false;
    },
});
