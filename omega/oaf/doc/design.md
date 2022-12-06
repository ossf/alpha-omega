# Overall Goals

(This document is a work-in-progress.)

We want to provide consumers of OSS a better ability to make informed choices about
the security posture of what they use. More specifically, we care about providing
information about *assurance activities* that have occurred that suggest that an
OSS project meets certain interesting criteria or carries a certain posture.

While we have opinions on the mapping between evidence ("activity X was performed with
Y result,") and posture ("and therefore Z is safe to use"), we think it's important
to have an extensible design, so that that others can bring their own assertions,
evidence, and policy mappings.

**GOAL:** Allow others to generate assertions and define policies that evaluate them.**

We're also aware of similar approaches with a related goal -- including SCITT,
Sigstore, in-toto, SPDX, and others. We are not attempting to compete with any
of them, since to the best of our knowledge, none of them directly target the space
we are.

**GOAL:** Integrate with existing standards, including in-toto assertions and SCITT.

Once assertions are created, they're only of value if they can be validated to be
authentic. This will be handled by those existing standards, like in-toto assertions.

But they also need to be actually usable; for this, we need a policy evaluation
capability - to define what criteria is expected in order for a target to "pass".
For this, we've chosen a reference implementation through REGO (part of
OpenPolicyAgent). However, nothing prevents others from using another policy
engine or writing their own. Assertions are *just* JSON.

**GOAL:** Provide a reference implementation focusing on end-to-end usability.

# Project Status

This project is in the early stages of incubation. It is not ready for any real-world
usage. We welcome new folks who would like to participate and help drive this project
forward.

# Design Thoughts


## Assertions

The subject of an assertion can either by a physical assert (left-pad-1.3.0.tar.gz
retrieved from registry.npmjs.com) or a logic asset, like "left-pad". I suppose it
could also be a collection of assets, though defining the scope of the assertion
may be more difficult.

There are relationships between these subjects types:
* Packages are derived from Projects.
* Repositories are part of a Project.
* Files are contained in Packages.
* An Actor takes actions on Files, Repositories, Packages, and Projects.
* An Actor may be a person or an automated system or tool.

Other asset types may be defined later.

We want to assert that:

* An activity was performed targeting an asset
* The results of that activity was X.

For example, assertions could (conceptually) be:

1. A Repository was rated to the following Security Scorecard value.
2. A Repository has had a commit in the past year.
3. A Project declared that it's repository was <X>.
4. A Package was declared to be derived from a Repository.
5. A Package was successfully rebuilt from a Repository at commit <X>.
6. <Tool> was run against <Package> looking for <Rules> and identified <Results>.
7. A <File> was evaluated to have a hash <Hash>.

## Assertion Formats

Assertions need a few different parts:

* Subject: What is the thing that the assertion is targeting?
* Predicate: What are we saying about the subject?
* Metadata: Additional, relevant information about the production of the assertion.

