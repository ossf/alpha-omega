import argparse
import json
import logging
import sys

from assertion.assertion.base import BaseAssertion
from assertion.policy.base import BasePolicy
from assertion.policy.rego import RegoPolicy
from assertion.policy.result import ExecutionResult
from assertion.repository.base import BaseRepository
from assertion.signing.base import BaseSigner
from assertion.subject import BaseSubject
from assertion.utils import get_subclasses_recursive


class OAF:
    """Entrypoint into the Omege Assertion Framework CLI."""

    version = "0.1.0"

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="Omega Assertion Framework",
            description="Assurance assertions made easy.",
        )

        # Global Options
        self.parser.add_argument("--version", action="version", version="%(prog)s " + self.version)
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
        p_generate.add_argument('--input-file', help='Input file', type=str, required=False)
        p_generate.add_argument('--content', help='Content of assertion (for Manual assertions only)', type=str, required=False)
        p_generate.add_argument('--evidence', help='Evidence of assertion (for Manual assertions only)', type=str, required=False)

        p_generate.add_argument("--signer", help="Signature to use", type=str, required=False)
        p_generate.add_argument(
            "--repository",
            help="Repository to use (e.g. sqlite:assertions.db)",
            type=str,
            required=False,
        )

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
            help='Policy to use, or "all" for all available policies.',
            type=str,
            required=True,
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
                logging.error("Error generating assertion")
                sys.exit(1)

            assertion.emit()

            if args.signer:
                signer = BaseSigner.create_signer(args.signer)
                signer.sign(assertion)
                if not signer.verify(assertion.serialize("json")):
                    logging.error("Error verifying signature")
                    sys.exit(1)

            if args.repository:
                repository = BaseRepository.create_repository(args.repository)
                repository.add_assertion(assertion)
                print("Assertion added to repository.")
            else:
                print(assertion.serialize("json-pretty"))

            sys.exit(0)

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
        if args.policy == "all":
            rego = RegoPolicy(["assertion/policy/rego_policies"], None, signer)
        else:
            rego = RegoPolicy(["assertion/policy/rego_policies"], args.policy.split(","), signer)

        if not rego:
            logging.error("Error initializing Rego policy evaluator.")
            sys.exit(1)

        if not rego.policies:
            logging.error("No policies found.")
            sys.exit(1)

        results = rego.execute(assertions, None)
        for policy, result in results.items():
            print(f"[{'PASS' if result.passed else 'FAIL'}]: {policy}: {result.message}")

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
        def generate_assertion(assertion_type: str, subject_str: str, additional_args: argparse.Namespace) -> BaseAssertion:
            """Generates an assertion."""
            # pylint: disable=import-outside-toplevel
            # pylint: disable=unused-import
            from assertion.assertion.languages import ProgrammingLanguage
            from assertion.assertion.reproducible import Reproducible
            from assertion.assertion.securityadvisories import SecurityAdvisory
            from assertion.assertion.securityscorecards import SecurityScorecard
            from assertion.assertion.manual import Manual
            from assertion.assertion.securityreview import SecurityReview

            for cls in get_subclasses_recursive(BaseAssertion):
                logging.debug("Checking assertion class: %s", cls.__name__)

                if cls.__name__.lower() != assertion_type.strip().lower():
                    continue

                logging.debug("Instantiating assertion class %s", cls.__name__)
                subject = BaseSubject.create_subject(subject_str)

                additional_args = vars(additional_args)
                additional_args.pop("subject")
                assertion = cls(subject, **additional_args)  # type: BaseAssertion
                assertion.process()

                return assertion

            logging.debug(
                "Assertion not found. Use --list-assertions to see the full list of available assertions."
            )
            return None


if __name__ == "__main__":
    oaf = OAF()
    oaf.parse_args()
