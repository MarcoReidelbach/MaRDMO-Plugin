'''Pre-save validators for MaRDMO questionnaire values.

Each validator receives an RDMO ``Value`` instance and raises
``rest_framework.exceptions.ValidationError`` when the value is rejected.
Validators are registered in ``builders.py`` via ``build_presave_validator_map``.

Provides:

- :func:`validate_label_format`      — rejects entries not matching ``Label (Description)``
- :func:`validate_short_description` — rejects descriptions longer than 250 characters
- :func:`validate_qudt_id`           — rejects QUDT IDs not matching the expected format
- :func:`validate_properties`        — rejects mutually exclusive data-property combinations
'''

import re

from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from .helpers import extract_parts
from .getters import get_mathmoddb
from .model.constants import data_properties_check, data_properties_label

_QUDT_ID_RE = re.compile(r'^[A-Z][a-zA-Z_\-]*$')


def validate_label_format(instance):
    '''Reject values whose text cannot be parsed as ``Label (Description)``.

    Accepts empty text (field cleared), ``Label (Description)`` (user entry),
    and ``Label (Description) [source]`` (external entry).  Rejects anything
    else — unclosed parentheses, plain text without parentheses, etc. — because
    ``general.relation`` would silently ignore those anyway.

    Args:
        instance: RDMO ``Value`` instance about to be saved.

    Raises:
        ValidationError: when ``instance.text`` is non-empty and
            ``extract_parts`` cannot identify a source (``source == ""``).
    '''
    if not instance.text:
        return
    source = extract_parts(instance.text)[2]
    if source == '':
        raise ValidationError({
            'text': [_('Wrong format. Expected: Label (Description)')]
        })


def validate_short_description(instance):
    '''Reject a short description that exceeds 250 characters.

    Args:
        instance: RDMO ``Value`` instance about to be saved.

    Raises:
        ValidationError: when ``instance.text`` exceeds 250 characters.
    '''
    if instance.text and len(instance.text) > 250:
        raise ValidationError({
            'text': [_('Short description must not exceed 250 characters.')]
        })


def validate_qudt_id(instance):
    '''Reject a QUDT reference ID that does not match the expected format.

    The ID must start with an uppercase letter, optionally followed by letters,
    underscores, or hyphens (e.g. ``SpeedOfLight``, ``MassOfElectron``).
    A single uppercase letter is accepted to avoid false errors during incremental
    typing; completeness is enforced by the documentation checker.

    Skips validation when no option or no text is present — the option being
    set indicates the user has committed to a reference type; only then is the
    text format enforced.

    Args:
        instance: RDMO ``Value`` instance about to be saved.

    Raises:
        ValidationError: when both ``instance.option`` and ``instance.text``
            are set and ``instance.text`` does not match
            ``^[A-Z][a-zA-Z_\\-]*$``.
    '''
    if not instance.option or not instance.text:
        return
    if not _QUDT_ID_RE.match(instance.text):
        raise ValidationError({
            'text': [_(
                'Invalid QUDT ID. Must start with an uppercase letter'
                ' and contain only letters, underscores, or hyphens'
                ' (e.g. SpeedOfLight).'
            )]
        })


def validate_properties(instance):
    '''Reject a property option that creates a mutually exclusive pair.

    Collects all property option URIs already saved for the same entity page
    (same attribute and ``set_prefix``), adds the incoming option, then checks
    every pair in ``data_properties_check``.  Raises on the first conflict found.

    Skips the check when no option is attached to the instance (e.g. text-only
    saves that happen to land on the same attribute URI).

    The current instance is excluded from the DB query so that update operations
    (where the row already exists) are evaluated against the new option only.

    Args:
        instance: RDMO ``Value`` instance about to be saved.

    Raises:
        ValidationError: when the incoming option together with already-saved
            options contains a mutually exclusive pair from
            ``data_properties_check``.
    '''
    if not instance.option:
        return

    qs = instance.project.values.filter(
        snapshot   = None,
        attribute  = instance.attribute,
        set_prefix = instance.set_prefix,
    )
    if instance.pk:
        qs = qs.exclude(pk=instance.pk)

    existing_uris = set(qs.values_list('option__uri', flat=True))
    existing_uris.add(instance.option.uri)

    mathmoddb = get_mathmoddb()
    for key_a, key_b in data_properties_check:
        entry_a = mathmoddb.get(key=key_a)
        entry_b = mathmoddb.get(key=key_b)
        if entry_a and entry_b:
            if entry_a['url'] in existing_uris and entry_b['url'] in existing_uris:
                raise ValidationError({
                    'text': [format_lazy(
                        _(
                            'Inconsistent properties: {a} and {b}'
                            ' cannot both be selected.'
                        ),
                        a=data_properties_label[key_a],
                        b=data_properties_label[key_b],
                    )]
                })
