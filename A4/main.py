"""Run from any working directory. IFC inputs stay outside the Git repository."""
import argparse
import hashlib
import json
from pathlib import Path
import ifcopenshell
try:
    from .load_path import analyse, COMM_results
except ImportError:
    from load_path import analyse, COMM_results


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description='Screen potential geometric vertical load paths')
    parser.add_argument('--str', dest='str_path', type=Path, required=True)
    parser.add_argument('--geo', dest='geo_path', type=Path, required=True)
    parser.add_argument('--config', type=Path, default=here / 'config.json')
    parser.add_argument('--output', type=Path, default=here / 'output')
    parser.add_argument('--tolerance', type=float, help='Override screening tolerance in metres')
    args = parser.parse_args()
    for path in (args.str_path, args.geo_path, args.config):
        if not path.is_file():
            parser.error(f'File not found: {path}')
    config = json.loads(args.config.read_text(encoding='utf-8'))
    if args.tolerance is not None:
        config['tolerance_m'] = args.tolerance
    print('Reading IFC models and extracting geometry...', flush=True)
    elements, edges, rows = analyse(ifcopenshell.open(str(args.str_path)),
                                    ifcopenshell.open(str(args.geo_path)), config)
    summary = COMM_results(elements, edges, rows, config, args.output)
    provenance = {}
    for source, path in [('STR', args.str_path), ('GEO', args.geo_path)]:
        provenance[source] = {'filename': path.name,
                              'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    (args.output / 'inputs.json').write_text(json.dumps(provenance, indent=2), encoding='utf-8')
    print(json.dumps(summary['counts'], indent=2))
    print(f"Connections: {len(edges)}. Results: {args.output.resolve()}")


if __name__ == '__main__':
    main()

