"""Offline domain analysis and replay."""
import argparse
import json
from .io import create,verify,load
from .learning import compare

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);s=p.add_subparsers(dest='command',required=True)
    a=s.add_parser('analyze');a.add_argument('input');a.add_argument('--output',required=True)
    a=s.add_parser('verify');a.add_argument('bundle')
    a=s.add_parser('benchmark');a.add_argument('input')
    args=p.parse_args(argv)
    try:
        r=compare(load(args.input)) if args.command=='benchmark' else (create(args.output,load(args.input)) if args.command=='analyze' else verify(args.bundle))
        print(json.dumps(r,sort_keys=True,indent=2));return 1 if args.command=='analyze' and r['status']=='FAIL' else 0
    except (ValueError,TypeError,KeyError,OSError,RecursionError,OverflowError) as exc:p.error(str(exc))

if __name__=='__main__':raise SystemExit(main())
