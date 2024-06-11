from pathlib import Path

from fluent.runtime import FluentLocalization, FluentResourceLoader
from typing import Dict


SUPPORTED_LOCALES = ["ru", "en"]


def get_fluent_localization() -> Dict[str, FluentLocalization]:
    """
    Load locale files like 'ru_locale.ftl' from directory 'l10n' in $PATH
    :return: Dict[str, FluentLocalization]
    """

    locale_dir = Path(__file__).parent.joinpath("l10n")
    if not locale_dir.exists():
        error = "'l10n' directory not found"
        raise FileNotFoundError(error)
    if not locale_dir.is_dir():
        error = "'l10n' is not a directory"
        raise NotADirectoryError(error)

    locales_data = dict()
    for locale_name in SUPPORTED_LOCALES:
        locale_file = Path(locale_dir, f"{locale_name}_locale.ftl")
        if not locale_file.exists():
            error = f"{locale_name}_locale.ftl file not found"
            raise FileNotFoundError(error)

        l10n_loader = FluentResourceLoader(
            str(locale_file.absolute()),
        )

        locales_data[locale_name] = FluentLocalization(
            locales=[locale_name],
            resource_ids=[str(locale_file.absolute())],
            resource_loader=l10n_loader,
        )

    return locales_data
