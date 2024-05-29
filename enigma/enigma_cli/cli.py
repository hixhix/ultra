import argparse
from argparse import RawTextHelpFormatter
from enigma_cli.enigma_app_cli.enigma_app_cli import InteractiveEnigmaCli
from enigma_cli.enigma_cli.enigma_cli import CommandLineEnigmaCli
from enigma_cli.code_sheet_cli.code_sheet_cli import CodeSheetsCli
from enigma_cli.cyclometer_cli.cyclometer_cli import CyclometerCli
from enigma_cli.zygalski_sheets_cli.zygalski_sheets_cli import ZygalskiSheetsCli
from enigma_cli.bombe_machines_cli.bombe_menu_cli import BombeMenuCli
from enigma_cli.statistics_cli.statistics_cli import StatisticsCli
from enigma_cli.plugboard_optomizer_cli.plugboard_optomizer_cli import PlugboardOptomizerCli
from enigma_cli.ring_settings_optomizer_cli.ring_settings_optomizer_cli import RingSettingsOptomizerCli


def enigma_cli(argv=None):

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    # interactive enigma
    # command line enigma
    # code sheet
    # statistics
    #    bigram count
    #    trigram count
    #    index of coincidence
    # zygalski sheets
    #    svg zygalsi sheets
    #    svg zygalski sheets solution
    #    text zygalski sheets
    #    indicators generator
    #    permutations filter
    #    wehrmacht catalog
    # bombe machine
    #    turing welchman bombe
    #    ring settings optomizer

    subparsers.add_parser(
        'interactive_enigma',
        help="interactive enigma")
    interactive_enigma_cli = InteractiveEnigmaCli()

    command_line_enigma = subparsers.add_parser(
        'enigma_simulator',
        help='cli enigma',
        formatter_class=RawTextHelpFormatter)
    command_line_enigma_cli = CommandLineEnigmaCli(command_line_enigma)

    code_sheets = subparsers.add_parser(
        'code_sheets',
        help='code sheets')
    code_sheets_cli = CodeSheetsCli(code_sheets)

    cyclometer = subparsers.add_parser(
        'cyclometer',
        help='cyclometer menu')
    cyclometer_cli = CyclometerCli(cyclometer)

    zygalski_sheets = subparsers.add_parser(
        'zygalski_sheets',
        help='zygalski sheets menu')
    zygalski_sheets_cli = ZygalskiSheetsCli(zygalski_sheets)

    bombe_machine = subparsers.add_parser(
        'bombe_machine',
        help='bombe machine menu')
    bombe_machine_cli = BombeMenuCli(bombe_machine)

    ring_settings_optomizer = subparsers.add_parser(
        'ring_optomizer',
        help='ring settings optomizer menu')
    ring_settings_optomizer_cli = RingSettingsOptomizerCli(ring_settings_optomizer)

    plugboard_optomizer = subparsers.add_parser(
        'pb_optomizer',
        help='Plugboard optomizer menu')
    plugboard_optomizer_cli = PlugboardOptomizerCli(plugboard_optomizer)

    statistics = subparsers.add_parser(
        'statistics',
        help='statistics menu')
    statistics_cli = StatisticsCli(statistics)

    args = parser.parse_args(argv)
    args = vars(args)

    if args['command'] == 'interactive_enigma':
        interactive_enigma_cli.process_args(args)

    elif args['command'] == 'enigma_simulator':
        command_line_enigma_cli.process_args(args)

    elif args['command'] == 'code_sheets':
        code_sheets_cli.process_args(args)

    elif args['command'] == 'cyclometer':
        cyclometer_cli.process_args(args)

    elif args['command'] == 'zygalski_sheets':
        zygalski_sheets_cli.process_args(args)

    elif args['command'] == 'bombe_machine':
        bombe_machine_cli.process_args(args)
    
    elif args['command'] == 'ring_optomizer':
        ring_settings_optomizer_cli.process_args(args)

    elif args['command'] == 'pb_optomizer':
        plugboard_optomizer_cli.process_args(args)

    elif args['command'] == 'statistics':
        statistics_cli.process_args(args)

    return 0