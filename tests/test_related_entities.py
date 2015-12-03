def test_add_related_entities(related_entity_container, related_type, related_name):
    related_entity_container.add_related_entity(related_type, related_name)
    assert related_entity_container.refresh().related == [
        {'type': related_type, 'name': related_name}
    ]
