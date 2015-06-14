import Ember from 'ember';

export default Ember.Component.extend({

    errors_caption: function() {
        let num_errors = this.get('test.num_errors');
        return 'Errors (' + num_errors + ')';
    }.property('test')
});
