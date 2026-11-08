"""Compute persistent H0/H1 and fixed-scale features from a JSON point cloud."""
import argparse
import json
from pathlib import Path
from . import persistence, features, barcode_svg


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path)
    parser.add_argument('--max-edge',type=float,default=2.0)
    parser.add_argument('--scales',nargs='+',type=float,default=[0.2,0.6,1.1,1.8])
    parser.add_argument('--output',type=Path)
    parser.add_argument('--svg',type=Path)
    args=parser.parse_args(argv)
    try:
        data=json.loads(args.input.read_text(encoding='utf-8'))
        if not isinstance(data,dict): raise ValueError('Input must be a JSON object with points')
        report=persistence(data['points'],args.max_edge)
        report['features']=features(report,args.scales)
        encoded=json.dumps(report,indent=2,allow_nan=False)+'\n'
        for path,content in [(args.output,encoded),(args.svg,barcode_svg(report))]:
            if path:
                path.parent.mkdir(parents=True,exist_ok=True); path.write_text(content,encoding='utf-8')
        print(encoded,end='')
    except (OSError,ValueError,KeyError,TypeError,OverflowError) as exc:
        parser.error(str(exc))


if __name__=='__main__': main()
