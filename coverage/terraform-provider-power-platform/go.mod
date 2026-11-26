// Reads a checkout of terraform-provider-power-platform and writes the coverage
// mapping for this corpus. A module of its own so the corpus has no Go module at
// its root.
module github.com/AdamCoulterOz/powerplatform-apis/coverage/terraform-provider-power-platform

go 1.26.0

require golang.org/x/tools v0.48.0

require (
	golang.org/x/mod v0.39.0 // indirect
	golang.org/x/sync v0.22.0 // indirect
)
