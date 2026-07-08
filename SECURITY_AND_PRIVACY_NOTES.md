# Security and privacy notes

This repository was prepared as a public-facing manuscript and reproducibility snapshot. Known server-specific details were removed from command wrappers/configs where possible. Before and after public release, maintainers should continue to avoid adding:

- absolute local paths
- usernames and hostnames
- IP addresses or private server names
- API tokens or passwords
- private review drafts or AI-cowork text that is not intended for release
- non-public manuscript administrative notes
- source PDFs, validation PDFs, restricted source archives, or other non-redistributable raw materials

The retained R02A source assignment and downstream manifests are included because they are needed to trace the reported hard-split stress-test analyses.

## Current-tree scrub status

The current release-intended file tree has been reviewed for known private-path, credential-like, restricted-source, and draft-marker concerns. No intentionally distributed source PDFs, validation PDFs, FASTA/FA raw source files, CIF files, credentials, API tokens, or concrete private execution paths were identified in the public-facing file tree.

This note does not replace future safety review if new files are added. Any future release should repeat the public-safety scan before tagging and archiving.

## Release-history note

This public-release metadata patch updates the current `main` tree. If maintainers later discover that earlier Git history contains sensitive artifacts, the public archive should instead be generated from a clean snapshot or a history-cleaned repository before wider dissemination.


## DOI-sync release note

After public release and Zenodo archival, the repository citation metadata was synchronized with GitHub release `v1.0.1` and Zenodo DOI https://doi.org/10.5281/zenodo.21254963. Future releases should repeat repository validation, checksum verification, and public-safety review before archive DOI generation.
