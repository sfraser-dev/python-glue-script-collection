import argparse

# Import custom modules
import MySubs1.create_output_filename
import MySubs5.create_cornix_free_text_advanced_template
import MySubs10.read_trade_config_file
import MySubs11.create_cornix_free_text_simple_template
import MySubs12.get_cornix_client_name
import MySubs13.check_values_from_config_file


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate Cornix templates')
    parser.add_argument('file', help='Config file path')
    parser.add_argument('--ewf', help='Entries weighting factor', default=0)
    parser.add_argument('--twf', help='Targets weighting factor', default=0)
    parser.add_argument('--aoe', help='Amount of entries (override config file number of entries)', default=0)
    parser.add_argument('--nota', help='Number of targets (override config file number of targets)', default=0)
    parser.add_argument('--dev', help='Dynamic entry value for dynamic risk fixed position size', default=0)

    args = parser.parse_args()

    # Read trade config file
    config_hash = read_trade_config_file(args.file)

    # Override number of entries/targets if provided on command line
    if args.aoe:
        config_hash['numberOfEntries'] = args.aoe
    if args.nota:
        config_hash['numberOfTargets'] = args.nota

    # Check if entries and targets make sense and determine trade type
    trade_type = check_values_from_config_file(
        config_hash['numberOfEntries'],
        config_hash['numberOfTargets'],
        config_hash['highEntry'],
        config_hash['lowEntry'],
        config_hash['highTarget'],
        config_hash['lowTarget'],
        config_hash['stopLoss'],
        config_hash['leverage'],
        config_hash['noDecimalPlacesForEntriesTargetsAndSLs'],
        config_hash['wantedToRiskAmount']
    )

    # Generate Cornix templates
    cornix_template_simple = create_cornix_free_text_simple_template(
        config_hash['coinPair'],
        config_hash['leverage'],
        config_hash['highEntry'],
        config_hash['lowEntry'],
        config_hash['highTarget'],
        config_hash['lowTarget'],
        config_hash['stopLoss'],
        config_hash['noDecimalPlacesForEntriesTargetsAndSLs'],
        config_hash['numberOfEntries'],
        config_hash['numberOfTargets'],
        trade_type
    )

    cornix_template_advanced = create_cornix_free_text_advanced_template(
        config_hash['coinPair'],
        get_cornix_client_name(config_hash['client']),
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
        trade_type,
        args.ewf,
        args.twf,
        args.dev
    )

    # Print templates to screen
    print(cornix_template_simple)
    print(cornix_template_advanced)

    # Print template to file
    output_filename = create_output_filename(args.file, config_hash['coinPair'], trade_type)
    with open(output_filename, 'w') as fh:
        print(cornix_template_simple, file=fh)
        print(cornix_template_advanced, file=fh)


if __name__ == '__main__':
    main()

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
cornix_template_simple = create_cornix_free_text_simple_template(config_hash["coinPair"], config_hash['leverage'], config_hash['highEntry'], config_hash['lowEntry'], config_hash['highTarget'], config_hash['lowTarget'], config_hash['stopLoss'], config_hash['noDecimalPlacesForEntriesTargetsAndSLs'], config_hash['numberOfEntries'], config_hash['numberOfTargets'], is_trade_a_long)
cornix_template_advanced = create_cornix_free_text_advanced_template(config_hash['coinPair'], config_hash['client'], config_hash['leverage'], config_hash['numberOfEntries'], config_hash['highEntry'], config_hash['lowEntry'], config_hash['numberOfTargets'], config_hash['highTarget'], config_hash['lowTarget'], config_hash['stopLoss'], config_hash['noDecimalPlacesForEntriesTargetsAndSLs'], config_hash['wantedToRiskAmount'], is_trade_a_long, args.ewf, args.twf, args.dev)

# Print templates to screen
print(*cornix_template_simple, sep='\n')
print(*cornix_template_advanced, sep='\n')

# Create output file name
script_name = os.path.basename(sys.argv[0])
output_file_name = create_output_filename(script_name, config_hash['coinPair'], is_trade_a_long)

# Write templates to file
with open(output_file_name, 'w') as f:
    f.writelines(cornix_template_simple + cornix_template_advanced)

