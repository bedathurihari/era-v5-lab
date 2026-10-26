"""Validate G5 configs: report missing values and provenance, reject unauthorized nulls."""
from pathlib import Path
import argparse
import re
import sys
import yaml

PENDING_PREFIXES = {
    'architecture.kronecker_pos_dim', 'architecture.ke2_output_shape',
    'architecture.vocab_size', 'architecture.hidden_size',
    'architecture.num_layers', 'architecture.num_heads',
    'architecture.num_experts', 'architecture.top_k',
    'architecture.max_context', 'training.learning_rate',
    'training.batch_size', 'training.steps',
}

def check(path: Path) -> int:
    raw = path.read_text(encoding='utf-8')
    errors = []
    pending = []
    mapping = []
    try:
        data = yaml.safe_load(raw)
        if not isinstance(data, dict): errors.append('root must be a YAML mapping')
    except yaml.YAMLError as exc:
        errors.append(f'YAML syntax: {exc}')
    for lineno, line in enumerate(raw.splitlines(), 1):
        if not line.strip() or line.lstrip().startswith('#'): continue
        m = re.match(r'^(\s*)([\w-]+):(?:\s*(.*))?$', line)
        if not m:
            errors.append(f'line {lineno}: unsupported YAML structure or missing key')
            continue
        indent, key, rest = len(m[1]), m[2], m[3] or ''
        while mapping and mapping[-1][0] >= indent: mapping.pop()
        qualified = '.'.join([v for _, v in mapping] + [key])
        value = rest.split('#', 1)[0].strip()
        comment = rest.split('#', 1)[1].strip() if '#' in rest else ''
        if not value:
            if comment: errors.append(f'line {lineno}: {qualified} missing value')
            else: mapping.append((indent, key))
            continue
        if not re.search(r'\bsource\s*:', comment, re.I):
            errors.append(f'line {lineno}: {qualified} missing source comment')
        if value in ('null', '~', 'None'):
            pending.append(f'line {lineno}: {qualified} has no value')
            if qualified not in PENDING_PREFIXES or 'source:' not in comment:
                errors.append(f'line {lineno}: {qualified} unauthorized unresolved value')
    print('Missing values / pending dependencies:')
    for issue in pending: print('  PENDING:', issue)
    print('Missing source / validation errors:')
    for issue in errors: print('  ERROR:', issue)
    print(f'Errors: {len(errors)}; pending: {len(pending)}')
    return len(errors)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('config', nargs='?', default=str(Path(__file__).resolve().parents[1] / 'configs/config_v0.yaml'))
    args = parser.parse_args()
    sys.exit(1 if check(Path(args.config)) else 0)
