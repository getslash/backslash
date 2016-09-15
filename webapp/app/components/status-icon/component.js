import Ember from 'ember';

export default Ember.Component.extend({
    status: null,
    spaced: true,
    classNames: 'status-icon',
    classNameBindings: ['spaced:spaced', 'status'],
    tagName: 'span',
});
