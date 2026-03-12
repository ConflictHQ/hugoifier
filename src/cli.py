"""
Hugo-ifier CLI Tool

Usage examples:
  python cli.py complete themes/revolve-hugo
  python cli.py complete themes/revolve-hugo --output /tmp/my-site
  HUGOIFIER_BACKEND=openai python cli.py complete themes/revolve-hugo
  python cli.py analyze themes/revolve-hugo
  python cli.py hugoify themes/revolve-hugo
  python cli.py decapify output/revolve-hugo
"""

import argparse
import sys
import os

# Ensure src/ is on the path when called directly
sys.path.insert(0, os.path.dirname(__file__))

from utils.analyze import analyze
from utils.complete import complete
from utils.cloudflare import configure_cloudflare
from utils.deploy import deploy
from utils.hugoify import hugoify
from utils.decapify import decapify
from utils.translate import translate
from utils.parser import parse


def main():
    parser = argparse.ArgumentParser(
        description="Hugo-ifier — AI-powered Hugo theme converter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        '--backend', choices=['anthropic', 'openai', 'google'],
        help='AI backend to use (overrides HUGOIFIER_BACKEND env var)',
    )
    subparsers = parser.add_subparsers(dest="command")

    # complete — full pipeline
    complete_parser = subparsers.add_parser("complete", help="Run the full pipeline (analyze → hugoify → decap)")
    complete_parser.add_argument("path", help="Path to the theme directory")
    complete_parser.add_argument("--output", "-o", help="Output directory (default: output/{theme-name})")
    complete_parser.add_argument("--cms-name", default=None, help="Whitelabel CMS name")
    complete_parser.add_argument("--cms-logo", default=None, help="Whitelabel logo URL")
    complete_parser.add_argument("--cms-color", default=None, help="Whitelabel top-bar hex color")

    # analyze
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a theme and report structure")
    analyze_parser.add_argument("path", help="Path to the theme")

    # hugoify
    hugoify_parser = subparsers.add_parser("hugoify", help="Convert HTML to Hugo theme (or validate existing Hugo theme)")
    hugoify_parser.add_argument("path", help="Path to HTML file or theme directory")

    # decapify
    decapify_parser = subparsers.add_parser("decapify", help="Add Decap CMS to an assembled Hugo site")
    decapify_parser.add_argument("path", help="Path to the Hugo site directory")
    decapify_parser.add_argument("--cms-name", default=None, help="Whitelabel CMS name (default: 'Content Manager')")
    decapify_parser.add_argument("--cms-logo", default=None, help="Whitelabel logo URL")
    decapify_parser.add_argument("--cms-color", default=None, help="Whitelabel top-bar hex color")

    # translate
    translate_parser = subparsers.add_parser("translate", help="Translate content (stub)")
    translate_parser.add_argument("path", help="Path to the content")

    # parse / lint
    parser_parser = subparsers.add_parser("parser", help="Parse and lint (stub)")
    parser_parser.add_argument("path", help="Path to the theme")

    # deploy (stub)
    deploy_parser = subparsers.add_parser("deploy", help="Deploy to Cloudflare (stub)")
    deploy_parser.add_argument("path", help="Path to the site")
    deploy_parser.add_argument("zone", help="Cloudflare zone")

    # cloudflare (stub)
    cloudflare_parser = subparsers.add_parser("cloudflare", help="Configure Cloudflare (stub)")
    cloudflare_parser.add_argument("path", help="Path to the site")
    cloudflare_parser.add_argument("zone", help="Cloudflare zone")

    args = parser.parse_args()

    # Override backend if specified on command line
    if args.backend:
        import config as cfg
        cfg.BACKEND = args.backend

    if args.command == "complete":
        result = complete(
            args.path,
            output_dir=getattr(args, 'output', None),
            cms_name=getattr(args, 'cms_name', None),
            cms_logo=getattr(args, 'cms_logo', None),
            cms_color=getattr(args, 'cms_color', None),
        )
        print(result)
    elif args.command == "analyze":
        print(analyze(args.path))
    elif args.command == "hugoify":
        print(hugoify(args.path))
    elif args.command == "decapify":
        print(decapify(
            args.path,
            cms_name=getattr(args, 'cms_name', None),
            cms_logo=getattr(args, 'cms_logo', None),
            cms_color=getattr(args, 'cms_color', None),
        ))
    elif args.command == "translate":
        print(translate(args.path))
    elif args.command == "parser":
        print(parse(args.path))
    elif args.command == "deploy":
        print(deploy(args.path, args.zone))
    elif args.command == "cloudflare":
        print(configure_cloudflare(args.path, args.zone))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
