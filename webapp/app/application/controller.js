import Ember from 'ember';

export default Ember.Controller.extend({

    gravatar_img_url: function() {

        let email = this.get('session.content.user_info.email');
        console.log('Getting gravatar for' + email);
        return 'http://www.gravatar.com/avatar/' + window.md5(email) + '?s=20';
    }.property('session.content.user_info.email')
});
