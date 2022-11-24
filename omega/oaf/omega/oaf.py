#!/usr/bin/env python
"""
Main entrypoint for the Omega Assertion Framework CLI.
"""
import argparse
import glob
import json
import importlib
import logging
import sys

from assertion.assertion.base import BaseAssertion
from assertion.policy import BasePolicy, DynamicPolicy, ResultState
from assertion.repository.base import BaseRepository
from assertion.signing.base import BaseSigner
from assertion.subject import BaseSubject
from assertion.utils import get_subclasses_recursive, ComplexJSONEncoder


class OAF:
    """Entrypoint into the Omega Assertion Framework CLI."""

    VERSION = "0.1.0"

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="Omega Assertion Framework", description="Assurance assertions made easy."
        )

        # Global Options
        self.parser.add_argument("--version", action="version", version="%(prog)s " + self.VERSION)
        self.parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

        subparsers = self.parser.add_subparsers(dest="command")

        # Generate Assertions
        p_generate = subparsers.add_parser("generate", help="Generate assertions")
        p_generate.add_argument(
            "--extension-dir",
            help="Path to additional extensions",
            type=str,
            required=False,
        )
        p_generate.add_argument(
            "--list-assertions", help="List available assertions", action="store_true"
        )
        p_generate.add_argument("--assertion", help="Type of assertion to generate", type=str)
        p_generate.add_argument(
            "--subject",
            help="Subject of assertion (PackageURL or GitHub repository)",
            type=str,
        )
        p_generate.add_argument("--input-file", help="Input file", type=str, required=False)
        p_generate.add_argument(
            "--content",
            help="Content of assertion (for Manual assertions only)",
            type=str,
            required=False,
        )
        p_generate.add_argument(
            "--evidence",
            help="Evidence of assertion (for Manual assertions only)",
            type=str,
            required=False,
        )

        p_generate.add_argument("--signer", help="Signature to use", type=str, required=False)
        p_generate.add_argument(
            "--repository",
            help="Repository to use (e.g. sqlite:assertions.db)",
            type=str,
            required=False,
        )
        p_generate.add_argument("--expiration", help="Expiration date", type=str, required=False)

        # Consume Assertions
        p_consume = subparsers.add_parser("consume", help="Consume assertions")
        p_consume.add_argument(
            "--extension-dir",
            help="Path to additional extensions",
            type=str,
            required=False,
        )
        p_consume.add_argument(
            "--signer", help="Signature to use (e.g. public key file)", type=str, required=False
        )
        p_consume.add_argument("--expiration", help="Expiration date", type=str, required=False)
        p_consume.add_argument(
            "--repository",
            help="Assertion repository to use (e.g. sqlite:assertions.db)",
            type=str,
            required=True,
        )
        p_consume.add_argument(
            "--subject",
            help="Subject of assertion (PackageURL or GitHub repository)",
            type=str,
        )
        p_consume.add_argument(
            "--list-policies", help="List available policies", action="store_true"
        )
        p_consume.add_argument(
            "--policy",
            help='Policy glob to use, defaults to "builtin/**/*" for all built-in policies.',
            default=[],
            required=False,
            action="append",
        )

    def parse_args(self):
        """Parses arguments and starts the actions."""
        args = self.parser.parse_args()

        if args.verbose:
            logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")
        else:
            logging.basicConfig(
                level=logging.WARNING, format="%(asctime)s %(levelname)s %(message)s"
            )

        if args.command == "generate":
            self.parse_args_generate(args)
        elif args.command == "consume":
            self.parse_args_consume(args)
        else:
            self.parser.print_help()

    def parse_args_generate(self, args):
        """Parses arguments for the 'generate' command."""
        if args.extension_dir:
            print("Not implemented.")
            sys.exit(1)

        if args.list_assertions:
            OAF.Generate.list_assertions()
            sys.exit(1)

        if args.assertion and args.subject:
            assertion = OAF.Generate.generate_assertion(args.assertion, args.subject, args)
            if not assertion:
                logging.error("No assertion was generated.")
                sys.exit(1)

            assertion.finalize()
            assertion.emit()

            if args.signer:
                signer = BaseSigner.create_signer(args.signer)
                signer.sign(assertion)
                if not signer.verify(assertion.serialize("json")):
                    logging.error("Error verifying signature")
                    sys.exit(1)

            if args.repository:
                repository = BaseRepository.create_repository(args.repository)
                if repository.add_assertion(assertion):
                    print("Assertion added to repository.")
                    logging.debug(assertion.serialize("json-pretty"))
                else:
                    print("Error adding assertion to repository.")
            else:
                print(assertion.serialize("json-pretty"))

            sys.exit(0)
        else:
            print("An assertion and a subject must be specified.")
            sys.exit(1)

    def parse_args_consume(self, args):
        """Parses arguments for the 'consume' command."""
        if args.extension_dir:
            print("Not implemented.")
            sys.exit(1)

        if args.list_policies:
            policies = BasePolicy.find_policies()
            if policies:
                for policy in policies:
                    print(policy)
                sys.exit(0)
            else:
                print("No policies found.")
                sys.exit(1)

        # Subject
        subject = BaseSubject.create_subject(args.subject)
        if not subject:
            logging.error("Error creating subject")
            sys.exit(1)

        # Assertion Repository
        repository = BaseRepository.create_repository(args.repository)
        if not repository:
            logging.error("Error creating repository")
            sys.exit(1)

        # Signatures
        signer = BaseSigner.create_signer(args.signer)
        if not signer:
            logging.error("Error creating signer object.")
            sys.exit(1)

        # Loads the assertions
        assertions = repository.find_assertions(subject)
        if not assertions:
            logging.error("No assertions found for subject")
            sys.exit(1)

        # Apply the policies against the assertions
        if not args.policy:
            args.policy = ["builtin/**/*"]
        policy = DynamicPolicy(args.policy, signer)
        results = policy.execute_all(assertions)
        if results:
            results = list(
                filter(
                    lambda s: s.get("execution_result").state
                    in [ResultState.PASS, ResultState.FAIL],
                    results,
                )
            )
            print(json.dumps(results, indent=2, cls=ComplexJSONEncoder))
        else:
            print("No assertions found for subject.")
            sys.exit(1)

    class Generate:
        """Helper class for the 'generate' subcommand."""

        @staticmethod
        def list_assertions():
            """Lists all available assertions."""
            _classes = get_subclasses_recursive(BaseAssertion)
            if _classes:
                for _class in _classes:
                    print(_class.__name__)
            else:
                print("No assertion classes found.")

        @staticmethod
        def generate_assertion(
            assertion_type: str, subject_str: str, additional_args: argparse.Namespace
        ) -> BaseAssertion:
            """Generates an assertion."""
            for filename in glob.glob("assertion/assertion/**/*.py", recursive=True):
                try:
                    importlib.import_module(filename.replace("/", ".").replace(".py", ""))
                except Exception as msg:
                    logging.warning("Error importing assertion: %s", msg)

            assertion_subclasses = get_subclasses_recursive(BaseAssertion)
            logging.debug(
                "Found %d assertion subclasses: %s",
                len(assertion_subclasses),
                [c.__name__ for c in assertion_subclasses],
            )

            for cls in get_subclasses_recursive(BaseAssertion):
                if cls.__name__.lower() != assertion_type.strip().lower():
                    continue

                logging.debug("Instantiating assertion class %s", cls.__name__)
                subject = BaseSubject.create_subject(subject_str)

                additional_args = vars(additional_args)
                additional_args.pop("subject")
                assertion = cls(subject, **additional_args)  # type: BaseAssertion
                assertion.process()

                return assertion

            logging.warning(
                "Assertion [%s] not found. Use --list-assertions to see the full list"
                "of available assertions.",
                assertion_type,
            )
            return None


if __name__ == "__main__":
    oaf = OAF()
    oaf.parse_args()
