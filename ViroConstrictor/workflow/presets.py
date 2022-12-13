import difflib
import re
from typing import Tuple

aliases = {
    "SARSCOV2": ["SARS-COV-2", "SARS2", "COVID", "COV", "SARSCOV", "SARSCOV2"],
    "INFLUENZA": [
        "FLU",
        "INFLU",
        "INFLUENZA",
        "INFA",
        "INFB",
        "INFLUENZA_A",
        "INFLUENZA_B",
        "INF",
    ],
    # "MEASLES": ["MEASLES", "MEV", "MEASLES_VIRUS"],
    # "HPV": ["PAPILLOMA_VIRUS", "HPV"]
}

presets = {
    "DEFAULT": {
        "RawAlign_AdditionalSettings": "",
        "BaseBAMFilters": "-F 256 -F 512 -F 4 -F 2048",
        "ClipperSettings": "",
        "Fastp_PhredScore_cutoff_illumina": 20,
        "Fastp_PhredScore_cutoff_nanopore": 7,
        "Fastp_PhredScore_cutoff_iontorrent": 20,
        "Fastp_WindowSize_illumina": 5,
        "Fastp_WindowSize_nanopore": 20,
        "Fastp_WindowSize_iontorrent": 15,
        "Fastp_MinReadLength": 100,
        "CleanAlign_AdditionalSettings_nanopore": "",
        "CleanAlign_AdditionalSettings_illumina": "",
        "CleanAlign_AdditionalSettings_iontorrent": "",
    },
    "SARSCOV2": {
        "RawAlign_AdditionalSettings": "",
        "BaseBAMFilters": "-F 256 -F 512 -F 4 -F 2048",
        "ClipperSettings": "",
        "Fastp_PhredScore_cutoff_illumina": 20,
        "Fastp_PhredScore_cutoff_nanopore": 7,
        "Fastp_PhredScore_cutoff_iontorrent": 20,
        "Fastp_WindowSize_illumina": 5,
        "Fastp_WindowSize_nanopore": 20,
        "Fastp_WindowSize_iontorrent": 15,
        "Fastp_MinReadLength": 100,
        "CleanAlign_AdditionalSettings_nanopore": "-E2,0 -O8,24 -A4 -B4",
        "CleanAlign_AdditionalSettings_illumina": "",
        "CleanAlign_AdditionalSettings_iontorrent": "",
    },
    "INFLUENZA": {
        "RawAlign_AdditionalSettings": "--splice",
        "BaseBAMFilters": "-F 256 -F 512 -F 4 -F 2048",
        "ClipperSettings": "--exclude-spliced --spliced-length-threshold 50 --min-aligned-length 50",
        "Fastp_PhredScore_cutoff_illumina": 20,
        "Fastp_PhredScore_cutoff_nanopore": 7,
        "Fastp_PhredScore_cutoff_iontorrent": 20,
        "Fastp_WindowSize_illumina": 5,
        "Fastp_WindowSize_nanopore": 20,
        "Fastp_WindowSize_iontorrent": 15,
        "Fastp_MinReadLength": 100,
        "CleanAlign_AdditionalSettings_nanopore": "",
        "CleanAlign_AdditionalSettings_illumina": "",
        "CleanAlign_AdditionalSettings_iontorrent": "",
    },
    "MEASLES": {
        "RawAlign_AdditionalSettings": "",
        "BaseBAMFilters": "-F 256 -F 512 -F 4 -F 2048",
        "ClipperSettings": "",
        "Fastp_PhredScore_cutoff_illumina": 20,
        "Fastp_PhredScore_cutoff_nanopore": 7,
        "Fastp_PhredScore_cutoff_iontorrent": 20,
        "Fastp_WindowSize_illumina": 5,
        "Fastp_WindowSize_nanopore": 20,
        "Fastp_WindowSize_iontorrent": 15,
        "Fastp_MinReadLength": 100,
        "CleanAlign_AdditionalSettings_nanopore": "",
        "CleanAlign_AdditionalSettings_illumina": "",
        "CleanAlign_AdditionalSettings_iontorrent": "",
    },
    "HPV": {
        "RawAlign_AdditionalSettings": "",
        "BaseBAMFilters": "-F 256 -F 512 -F 4 -F 2048",
        "ClipperSettings": "",
        "Fastp_PhredScore_cutoff_illumina": 20,
        "Fastp_PhredScore_cutoff_nanopore": 7,
        "Fastp_PhredScore_cutoff_iontorrent": 20,
        "Fastp_WindowSize_illumina": 5,
        "Fastp_WindowSize_nanopore": 20,
        "Fastp_WindowSize_iontorrent": 15,
        "Fastp_MinReadLength": 100,
        "CleanAlign_AdditionalSettings_nanopore": "",
        "CleanAlign_AdditionalSettings_illumina": "",
        "CleanAlign_AdditionalSettings_iontorrent": "",
    },
}


def get_key_from_value(d: dict, value: str) -> str:
    """This function finds the key in a dictionary which has a value matching the input value.

    Parameters
    ----------
    d
        The dictionary to search.
    value
        The value to search for.

    Returns
    -------
    The key from the dictionary which has the input value.

    """
    for k, v in d.items():
        if value in v:
            return k


def match_preset_name(targetname: str, use_presets: bool) -> Tuple[str, float]:
    if not use_presets:
        return "DEFAULT", 0
    # regex to remove all special characters from targetname except underscores and dashes
    query = re.sub(r"[^_a-zA-Z0-9/-]+", "", targetname).upper()

    if query == "DEFAULT":
        return "DEFAULT"

    # flatten list of lists aliases.values() into a single list
    aliases_list = [item for sublist in aliases.values() for item in sublist]

    best_match = difflib.get_close_matches(query, aliases_list, cutoff=0.0, n=1)[0]
    score = difflib.SequenceMatcher(None, a=query, b=best_match).ratio()

    if score < 0.35:
        return "DEFAULT", 0
    matched_preset = get_key_from_value(aliases, best_match)
    return matched_preset, score


def get_preset_parameter(preset_name: str, parameter_name: str) -> str:
    return presets[preset_name][parameter_name]