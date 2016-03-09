import Ember from 'ember';

export default Ember.Controller.extend({

    /* Avatar */
    admin: true,
    moderator: false,
    large: true,

    use_real_email: false,

    real_email: function() {
        if (this.get('use_real_email')) {
            return 'spatz@psybear.com';
        }
        return null;
    }.property('use_real_email'),

    
});
