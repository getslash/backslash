import Ember from 'ember';
import KeyboardShortcuts from 'ember-keyboard-shortcuts/mixins/component';
import {timeout, task} from 'ember-concurrency';


let _keys = [
    {key: '.', action: 'open_quick_search', description: 'Opens quick jump'},
    {key: 'esc', action: 'close_boxes'},
    {key: 'ctrl+s', action: 'goto_sessions', description: 'Jump to Sessions view'},
    {key: 'ctrl+u', action: 'goto_users', description: 'Jump to Users view'},
    {key: '?', action: 'display_help', description: 'Show this help message'},
];

let _shortcuts = {};

_keys.forEach(function(k) {
    _shortcuts[k.key] = k.action;
});


export default Ember.Component.extend(KeyboardShortcuts, {
    help_displayed: false,

    keyboardShortcuts: _shortcuts,
    keys: _keys,


    search(query, _, callback) {
        this.get('async_search').perform(query, callback);

    },

    select(obj) {
        let self = this;
        console.log('selecting', obj);

        self.sendAction('close_boxes');
        self._close_boxes();
        self.router.transitionTo(obj.type, obj.key);

    },

    async_search: task(function * (query, callback) {
        yield timeout(400);
        let res = yield this.api.call('quick_search', {term: query});
        callback(res.result);
    }).restartable(),

    _close_boxes() {
        let element = Ember.$('#goto-input');
        element.typeahead('destroy');
        element.off();
        this.set('quick_search_open', false);
        this.set('help_displayed', false);
    },

    actions: {

        close_boxes() {
            this._close_boxes();
        },

        display_help() {
            this.set('help_displayed', true);
        },

        goto_sessions() {
            this.router.transitionTo('sessions');
        },

        goto_users() {
            this.router.transitionTo('users');
        },


        open_quick_search() {
            let self = this;
            self.set('quick_search_open', true);
            Ember.run.later(function() {
                let element = Ember.$('#goto-input');
                element.typeahead({
                    hint: true,
                    highlight: true,
                    minLength: 1,
                }, {
                    name: 'Users',
                    source: self.search.bind(self),
                    display: 'name',
                    templates: {
                        suggestion: function(obj) {
                            let icon;
                            if (obj.type === 'subject') {
                                icon = 'rocket';
                            } else if (obj.type === 'user') {
                                icon = 'user';
                            }


                            return `<div><i class="fa fa-${icon}"></i> ${obj.name}</div>`;
                        },
                    },
                });
                element.on('focusout', function() {
                    self.sendAction('close_boxes');
                }).on('typeahead:selected', function(evt, obj) {
                    self.select(obj);
                }).on('typeahead:render', function() {
                    element.parent().find('.tt-selectable:first').addClass('tt-cursor');
                }).focus();
            });
        },
    }

});
