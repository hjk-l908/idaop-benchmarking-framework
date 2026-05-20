# Security and privacy notes

This Phase 2 repository was prepared as a public-facing draft. Known server-private details were removed from command wrappers/configs where possible. Before public release, perform a final scrub for:

- absolute local paths
- usernames and hostnames
- IP addresses or private server names
- API tokens or passwords
- private AI cowork review text that is not intended for release
- non-public manuscript administrative notes

The retained R02A source assignment and downstream manifests are included because they are needed to trace the reported hard-split stress-test analyses.
## Release-history policy

This private repository is treated as a staging repository. Before public release, the public-facing version should be created from a clean snapshot or squashed release history after final safety review. This avoids exposing earlier private-path cleanup commits through public Git history.
## Current-tree scrub status

As of the current private staging snapshot, GitHub Code searches for known prior private execution-path markers returned no current files outside this scrub documentation.

This confirms that the current repository file tree no longer exposes known private execution-path strings. This does not replace the separate pre-public-release requirement to publish from a clean snapshot or squashed release history.
