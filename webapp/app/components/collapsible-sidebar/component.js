import Ember from 'ember';

export default Ember.Component.extend({

    classNames: ['container-fluid'],

    side: {side: true, main: false},
    main: {side: false, main: true},

    collapsed: false,
});
