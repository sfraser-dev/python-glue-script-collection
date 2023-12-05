import argparse
from os.path import basename

import MyPac.MySubs1 
import MyPac.MySubs2 
import MyPac.MySubs3 
import MyPac.MySubs5 
import MyPac.MySubs10 
import MyPac.MySubs11 
import MyPac.MySubs12 
import MyPac.MySubs13 

# Parse command line arguments
parser = argparse.ArgumentParser(description='Process command line arguments.')
parser.add_argument('--file', '-f', type=str, required=True, help='Filename')
parser.add_argument('--ewf', '-e', type=str, required=True, help='Entries weighting factor')
parser.add_argument('--twf', '-t', type=str, required=True, help='Targets weighting factor')
parser.add_argument('--aoe', '-a', type=str, help='Amount of entries (override config file number of entries)')
parser.add_argument('--nota', '-n', type=str, help='Number of targets (override config file number of targets)')
parser.add_argument('--dev', '-d', type=str, help='Dynamic entry value for dynamic risk fixed position size')
args = parser.parse_args()

path_to_file = args.file
weighting_factor_entries = args.ewf
weighting_factor_targets = args.twf
number_of_entries_command_line = args.aoe
number_of_targets_command_line = args.nota
dynamic_entry_value = args.dev

# Set default values if not provided
if not number_of_entries_command_line:
    number_of_entries_command_line = 0

if not number_of_targets_command_line:
    number_of_targets_command_line = 0

if not dynamic_entry_value:
    dynamic_entry_value = 0

# Read trade file
config_hash = MyPac.MySubs10.read_trade_config_file (path_to_file)

# Override values if given on the command line
if number_of_entries_command_line != 0:
    config_hash['numberOfEntries'] = number_of_entries_command_line

if number_of_targets_command_line != 0:
    config_hash['numberOfTargets'] = number_of_targets_command_line

# Check entries and targets logical sense & determine if trade is a long or a short
is_trade_a_long = MyPac.MySubs13.check_values_from_config_file(config_hash['numberOfEntries'],
                                            config_hash['numberOfTargets'],
                                            config_hash['highEntry'],
                                            config_hash['lowEntry'],
                                            config_hash['highTarget'],
                                            config_hash['lowTarget'],
                                            config_hash['stopLoss'],
                                            config_hash['leverage'],
                                            config_hash['noDecimalPlacesForEntriesTargetsAndSLs'],
                                            config_hash['wantedToRiskAmount'])

# Generate Cornix Free Text templates
cornix_template_simple = MyPac.MySubs11.create_cornix_free_text_simple_template(config_hash['coinPair'],
                                                            config_hash['leverage'],
                                                            config_hash['highEntry'],
                                                            config_hash['lowEntry'],
                                                            config_hash['highTarget'],
                                                            config_hash['lowTarget'],
                                                            config_hash['stopLoss'],
                                                            config_hash['noDecimalPlacesForEntriesTargetsAndSLs'],
                                                            config_hash['numberOfEntries'],
                                                            config_hash['numberOfTargets'],
                                                            is_trade_a_long)

cornix_template_advanced = MyPac.MySubs5.create_cornix_free_text_advanced_template(config_hash['coinPair'],
                                                                MyPac.MySubs12.get_cornix_client_name(config_hash['client']),
                                                                config_hash['leverage'],
                                                                config_hash['numberOfEntries'],
                                                                config_hash['highEntry'],
                                                                config_hash['lowEntry'],
                                                                config_hash['numberOfTargets'],
                                                                config_hash['highTarget'],
                                                                config_hash['lowTarget'],
                                                                config_hash['stopLoss'],
                                                                config_hash['noDecimalPlacesForEntriesTargetsAndSLs'],
                                                                config_hash['wantedToRiskAmount'],
                                                                is_trade_a_long,
                                                                weighting_factor_entries,
                                                                weighting_factor_targets,
                                                                dynamic_entry_value)

# Print templates to screen
print('\n'.join(cornix_template_simple))
print('\n'.join(cornix_template_advanced))

# Print templates to file
script_name = basename(__file__)
file_name = MyPac.MySubs1.create_output_filename(script_name, config_hash['coinPair'], is_trade_a_long)
with open(file_name, 'w') as file:
    print('\n'.join(cornix_template_simple), file=file)
    print('\n'.join(cornix_template_advanced), file=file)
