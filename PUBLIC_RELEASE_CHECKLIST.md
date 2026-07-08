# Public release checklist

Before making this repository public:

- Confirm repository name and GitHub URL.
- Review author names/order in `CITATION.cff`; ORCID identifiers are not listed in this repository snapshot per current author-side decision.
- Confirm final DOI, release date/tag, and archival citation metadata before public release.
- Choose final code/data license(s).
- Archive release on Zenodo or equivalent and fill DOI.
- Confirm target journal data/code availability wording.
- Current-tree private-path scrub pass has been documented in SECURITY_AND_PRIVACY_NOTES.md; searches for known prior private execution-path markers returned 0 current files outside the scrub documentation.
- Before public release, repeat a final public-safety review for passwords, API tokens, server IP addresses, internal hostnames, private paths, private review drafts, and other non-release notes.
- Decide whether binary embedding files should be included in GitHub or only in an archival release.
- Add final manuscript citation once available.
- Before public release, publish from a clean snapshot or squashed public-release history; do not directly make the private staging repository public if earlier commits contained private paths or server-specific cleanup.
- Confirm whether a separate `DATA_LICENSE.md` should be retained alongside the final code `LICENSE`.
