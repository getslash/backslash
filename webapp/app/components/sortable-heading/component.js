import Ember from 'ember';

export default Ember.Component.extend({
    tagName: 'th',
    classNames: ['clickable'],

    sort: null,

    click() {
        this.sendAction('set_sort', this.get('sort_field'));
    },

    title: null,

    name: null,

    sort_field: function() {

        let name = this.get('name');

        if (name) {
            return name;
        }

        let title = this.get('title');

        if (!title) {
            return null;
        }

        return title.toLowerCase().replace(" ", "_");
    }.property('title')
});
