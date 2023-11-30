import argparse
import os
import sys

from MySubs1 import create_output_filename
from MySubs5 import create_cornix_free_text_advanced_template
from MySubs6 import get_cornix_client_name
from MySubs10 import read_trade_config_file
from MySubs11 import create_cornix_free_text_simple_template
from MySubs12 import check_values_from_config_file
from MySubs13 import get_config_hash

# Parse command line arguments
parser = argparse.ArgumentParser(description='Generate Cornix Free Text templates')
parser.add_argument('--file', help='Path to trade config file', required=True)
parser.add_argument('--ewf', help='Entries weighting factor', type=float)
parser.add_argument('--twf', help='Targets weighting factor', type=float)
parser.add_argument('--aoe', help='Override number of entries', type=int)
parser.add_argument('--ont', help='Override number of targets', type=int)
parser.add_argument('--dev', help='Dynamic entry value', type=float)

args = parser.parse_args()

# Validate command line arguments
if not args.file:
    sys.exit('--file is required')

# Read trade config file
config_hash = get_config_hash(args.file)

# Override number of entries/targets if specified on the command line
if args.aoe:
    config_hash['numberOfEntries'] = args.aoe

if args.ont:
    config_hash['numberOfTargets'] = args.ont

# Check if trade is a long or a short
is_trade_a_long = check_values_from_config_file(**config_hash)

# Generate Cornix Free Text templates
cornix_template_simple = create_cornix_free_text_simple_template(**config_hash, is_trade_a_long)
cornix_template_advanced = create_cornix_free_text_advanced_template(**config_hash, is_trade_a_long, args.ewf, args.twf, args.dev)

# Print templates to screen
print(*cornix_template_simple, sep='\n')
print(*cornix_template_advanced, sep='\n')

# Create output file name
script_name = os.path.basename(sys.argv[0])
output_file_name = create_output_filename(script_name, config_hash['coinPair'], is_trade_a_long)

# Write templates to file
with open(output_file_name, 'w') as f:
    f.writelines(cornix_template_simple + cornix_template_advanced)

