import Ember from 'ember';

export default Ember.Component.extend({

    classNames: ['container-fluid', 'query-result', 'test', 'clickable'],
    test: null,

    click: function() {
        this.sendAction('goto_test', this.get('test'));
    }
});
 
