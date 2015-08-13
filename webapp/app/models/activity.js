import DS from 'ember-data';

export default DS.Model.extend({
    action_string: DS.attr(),
    timestamp: DS.attr(),
    user_email: DS.attr(),
    what: DS.attr(),

    message: function() {

        const what = this.get('what');
        switch (this.get('action_string')) {

            case 'archived': return 'archived this ' + what;
            case 'unarchived': return 'unarchived this ' + what;
            case 'investigated': return 'marked this ' + what + ' as investigated';
            case 'uninvestigated': return 'marked this ' + what + ' as not investigated';
            default: return '???';
        }

    }.property('action_string'),

    icon: function() {
        switch (this.get('action_string')) {
            case 'archived':
            case 'unarchived':
                return 'archive';
            case 'investigated':
                return 'check';
            case 'uninvestigated':
                return 'times';
        }
        return 'bullseye';
    }.property('action_string'),

    activity_icon_class: function() {
        return this.get('action_string');
    }.property('action_string')

});
