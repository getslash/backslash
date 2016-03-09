import Ember from 'ember';

export default Ember.Controller.extend({

    /* Avatar */
    admin: true,
    moderator: false,
    large: true,

    search: null,

    queryParams: ['search'],

    toggle_visible: function() {
        let term = this.get('search');
        Ember.$('.proofing-example h3').each(function() {
            let heading = Ember.$(this);
            console.log('text is', heading.text());
            if ((!term) || (heading.text().indexOf(term) !== -1)) {
                heading.parent().css('display', 'block');
            } else {
                heading.parent().css('display', 'none');
            }
        });

    }.observes('search').on('init'),

    use_real_email: false,

    real_email: function() {
        if (this.get('use_real_email')) {
            return 'spatz@psybear.com';
        }
        return null;
    }.property('use_real_email'),


});
