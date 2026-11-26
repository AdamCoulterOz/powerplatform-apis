# Terraform provider coverage

Works out which resources and data sources in
[terraform-provider-power-platform](https://github.com/microsoft/terraform-provider-power-platform)
call which operations in this corpus, and writes it to
`coverage/terraform-provider-power-platform.json`. `specs.json` names that file
as the catalogue's `coverage`, so the browser renders it as a coverage view.

The mapping answers questions the provider's code cannot be read for at a
glance: which operations nothing calls, which parts of the provider still depend
on the legacy BAPI, and which calls the provider makes that no spec here
describes.

## Why it lives here

The mapping is a join between the provider and this corpus. It started on a
branch of a provider fork, but the provider is Microsoft's and the corpus is
ours, so the tooling sits with the corpus and reads a checkout of the provider.
Nothing needs to land in the provider for this to work.

The **format** belongs to the [OAS browser](https://github.com/AdamCoulterOz/oas-browser),
which publishes the validator. This directory owns the **content** only, so there
is no conformance checker here. CI runs the browser's own.

## Running it

Needs a checkout of the provider. Pass it as an argument, or set
`TERRAFORM_PROVIDER`. The corpus is the repository this directory is in.

```sh
cd coverage/terraform-provider-power-platform
export TERRAFORM_PROVIDER=~/Code/GitHub/microsoft/terraform-provider-power-platform
go run ./callsites > sites.json
go run ./callgraph > artifacts.json
python3 serialise.py sites.json artifacts.json
```

The Go tools need the Go version the provider's `go.mod` asks for, because
`callgraph` type-checks the provider. It stops if any package fails to
type-check, rather than writing a mapping with call edges quietly missing.

The `terraform-provider-coverage` workflow does this daily against the
provider's `main`, and on any spec change here, and commits the result with the
provider commit it describes in the message.

### Expected findings

The browser's validator fails on every finding, and some findings are correct.
`expected-findings.txt` lists the ones that are known and right (today, three
rows from the `data_record` calls marked approximate below). CI fails only when that set
changes, in either direction, so a new finding is noticed and a fixed one gets
crossed off.

## How it works

**`callsites`** resolves every `api.Client.Execute` call in the provider to a
method, host, path template and api-version. It has no type information, so it works by following
the codebase's own URL-builder helpers, string constants and local variables.
It resolves 169 call sites.

**`callgraph`** type-checks the whole of the provider's `internal/` and walks from each
registered resource and data source down to those call sites, recording the
route taken and whether it passes through a conditional. The component list
comes from the provider's own `Resources()` and `DataSources()` rather than from
filenames, because a filename heuristic is a remembered list rather than a
derived one, and its failure mode is quiet: an earlier version of this tool
matched `resource_*.go` and silently dropped the one component whose file is
named `resources_*.go`.

**`serialise.py`** joins the two, resolves each call to an `operationId` in the
corpus, and emits the mapping. `resolve.py` holds the matching rule, which comes
from the contract: a templated segment in the spec matches any single segment in
the call, everything else must match exactly including case, and where several
operations match, the one matching on the most literal segments wins. That last
clause matters because the Dataverse spec documents a generic OData surface, and
without it `records_query` shadows every specific operation on that host.

## What it deliberately does not do

**It does not normalise away defects.** Two billing-policy calls once spelled a
path `/licensing/BillingPolicies` where the API spells it `billingPolicies`.
Those rows failed the catalogue check, correctly, until the provider was fixed
in microsoft/terraform-provider-power-platform#1257. A mapping that quietly corrected
them would be hiding a real defect inside the file whose job is describing what
the code does.

**It does not assert that two operations are the same.** Saying a BAPI operation
and a Power Platform API operation are equivalent is a claim about what the specs
describe, not about what this code calls. It belongs to the corpus, and encoding
it here would turn a mapping into an equivalence table that nothing validates.

**It does not guess.** Two call sites in `data_record` build their path by
conditional reassignment, and this analysis does not track branches. They carry
`approximate: true` rather than a plausible path, because a row that says it is
uncertain is worth more than a row that is quietly wrong.

## Reading the output

Every call carries a `coverage` and a `grade`.

`coverage` is `full` when the entrypoint always reaches the operation and
`partial` when it reaches it only on some code path, with a `note` naming the
route. It is derived from whether the call sits inside a conditional, which is a
property of the code rather than of any practitioner's configuration.

`grade` is `derived` throughout: every row is read out of the source by static
analysis, not seen executing. The vocabulary has room for `observed`, for rows
that are one day backed by recorded traffic.

`uncatalogued` holds calls no operation can name: two async continuations that
follow a `Location` header, and the practitioner-supplied URL the `rest`
components exist to issue.
