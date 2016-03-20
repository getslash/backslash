import Ember from 'ember';
import KeyboardShortcuts from 'ember-keyboard-shortcuts/mixins/component';
import {timeout, task} from 'ember-concurrency';

export default Ember.Component.extend(KeyboardShortcuts, {

    keyboardShortcuts: {
        '.' : 'open_quick_search',
        'esc': 'close_box',
    },

    close_box() {
        let element = Ember.$('#goto-input');
        element.typeahead('destroy');
        element.off();
        this.set('quick_search_open', false);
    },

    search(query, _, callback) {
        this.get('async_search').perform(query, callback);

    },

    select(obj) {
        let self = this;
        console.log('selecting', obj);

        self.close_box();
        self.router.transitionTo(obj.type, obj.key);

    },

    async_search: task(function * (query, callback) {
        yield timeout(400);
        let res = yield this.api.call('quick_search', {term: query});
        callback(res.result);
    }).restartable(),

    actions: {

        close_box() {
            this.close_box();
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
                    self.close_box();
                }).on('typeahead:selected', function(evt, obj) {
                    self.select(obj);
                }).on('typeahead:render', function() {
                    element.parent().find('.tt-selectable:first').addClass('tt-cursor');
                }).focus();
            });
        },
    }

});
