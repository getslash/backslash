import Ember from 'ember';

export default Ember.Controller.extend({

    gravatarURL: function() {

        let email = this.get('session.content.user_info.email');
        console.log('Getting gravatar for' + email);
        return 'http://www.gravatar.com/avatar/' + window.md5(email);

    }.property('session.content.user_info.email')
});
