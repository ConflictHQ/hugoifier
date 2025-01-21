"""
This script serves as the command-line interface (CLI) for the Hugo-ifier tool.
It provides various commands to analyze, convert, and deploy themes using the utility scripts.
"""

import argparse
from utils.analyze import analyze
from utils.complete import complete
from utils.cloudflare import configure_cloudflare
from utils.deploy import deploy
from utils.hugoify import hugoify
from utils.decapify import decapify
from utils.translate import translate
from utils.parser import parse


def main():
    parser = argparse.ArgumentParser(description="Hugo-ifier CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a theme")
    analyze_parser.add_argument("path", help="Path to the theme")

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Complete the workflow")
    complete_parser.add_argument("path", help="Path to the theme")

    # Cloudflare command
    cloudflare_parser = subparsers.add_parser("cloudflare", help="Configure Cloudflare")
    cloudflare_parser.add_argument("path", help="Path to the theme")
    cloudflare_parser.add_argument("zone", help="Cloudflare zone")

    # Deploy command
    deploy_parser = subparsers.add_parser("deploy", help="Deploy the theme")
    deploy_parser.add_argument("path", help="Path to the theme")
    deploy_parser.add_argument("zone", help="Cloudflare zone")

    # Hugoify command
    hugoify_parser = subparsers.add_parser("hugoify", help="Convert to Hugo theme")
    hugoify_parser.add_argument("path", help="Path to the theme")

    # Decapify command
    decapify_parser = subparsers.add_parser("decapify", help="Integrate Decap CMS")
    decapify_parser.add_argument("path", help="Path to the theme")

    # Translate command
    translate_parser = subparsers.add_parser("translate", help="Translate content")
    translate_parser.add_argument("path", help="Path to the content")

    # Parser command
    parser_parser = subparsers.add_parser("parser", help="Parse and lint")
    parser_parser.add_argument("path", help="Path to the theme")

    args = parser.parse_args()

    if args.command == "analyze":
        print(analyze(args.path))
    elif args.command == "complete":
        print(complete(args.path))
    elif args.command == "cloudflare":
        print(configure_cloudflare(args.path, args.zone))
    elif args.command == "deploy":
        print(deploy(args.path, args.zone))
    elif args.command == "hugoify":
        print(hugoify(args.path))
    elif args.command == "decapify":
        print(decapify(args.path))
    elif args.command == "translate":
        print(translate(args.path))
    elif args.command == "parser":
        print(parse(args.path))
    else:
        parser.print_help()


if __name__ == "__main__":
    main() 