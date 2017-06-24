def test_add_related_entities(related_entity_container, related_type, related_name):
    related_entity_container.add_related_entity(related_type, related_name)
    related = _get_related_entities(related_entity_container)
    assert len(related) == 1
    [entity] = related
    assert entity['entity_type'] == related_type
    assert entity['name'] == related_name


def _get_related_entities(related_entity_container):
    return related_entity_container.client.api.get(f'/rest/entities', params={f'{related_entity_container.type}_id': related_entity_container.id})['entities']
