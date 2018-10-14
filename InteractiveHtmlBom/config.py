"""Config object"""

import dialog.settings_dialog
import argparse


class Config:
    # Helper constants
    bom_view_choices = ['bom-only', 'left-right', 'top-bottom']
    layer_view_choices = ['F', 'FB', 'B']
    default_sort_order = [
        'C', 'R', 'L', 'D', 'U', 'Y', 'X', 'F', 'SW', 'A',
        '~',
        'HS', 'CNN', 'J', 'P', 'NT', 'MH',
    ]
    default_checkboxes = ['Sourced', 'Placed']
    html_config_fields = [
        'dark_mode', 'show_silkscreen', 'highlight_pin1', 'redraw_on_drag',
        'board_rotation', 'checkboxes', 'bom_view', 'layer_view', 'extra_fields'
    ]

    # Defaults

    # HTML section
    dark_mode = False
    show_silkscreen = True
    highlight_pin1 = False
    redraw_on_drag = True
    board_rotation = 0
    checkboxes = default_checkboxes
    bom_view = 1
    layer_view = 1
    open_browser = True

    # General section
    bom_dest_dir = './bom/'  # This is relative to pcb file directory
    component_sort_order = default_sort_order
    component_blacklist = []
    blacklist_virtual = True

    # Extra fields section
    netlist_file = None
    netlist_initial_directory = ''  # This is relative to pcb file directory
    extra_fields = []
    board_variant_field = ''
    board_variants = []
    dnp_field = ''

    def __init__(self):
        """Init with defaults"""
        pass

    def set_from_dialog(self, dlg):
        # type: (dialog.settings_dialog.SettingsDialog) -> None
        # Html
        self.dark_mode = dlg.html.darkModeCheckbox.IsChecked()
        self.show_silkscreen = dlg.html.showSilkscreenCheckbox.IsChecked()
        self.highlight_pin1 = dlg.html.highlightPin1Checkbox.IsChecked()
        self.redraw_on_drag = dlg.html.continuousRedrawCheckbox.IsChecked()
        self.board_rotation = dlg.html.boardRotationSlider.Value
        self.checkboxes = dlg.html.bomCheckboxesCtrl.Value
        self.bom_view = self.bom_view_choices[dlg.html.bomDefaultView.Selection]
        self.layer_view = self.layer_view_choices[
            dlg.html.layerDefaultView.Selection]
        self.open_browser = dlg.html.openBrowserCheckbox.IsChecked()

        # General
        self.bom_dest_dir = dlg.general.bomDirPicker.Path
        self.component_sort_order = dlg.general.componentSortOrderBox.GetItems()
        self.component_blacklist = dlg.general.blacklistBox.GetItems()
        self.blacklist_virtual = \
            dlg.general.blacklistVirtualCheckbox.IsChecked()

        # Extra fields
        self.netlist_file = dlg.extra.netlistFilePicker.Path
        self.extra_fields = list(dlg.extra.extraFieldsList.GetCheckedStrings())
        self.board_variant_field = dlg.extra.boardVariantFieldBox.Value
        self.board_variants = list(
                dlg.extra.boardVariantList.GetCheckedStrings())
        self.dnp_field = dlg.extra.dnpFieldBox.Value

    def transfer_to_dialog(self, dlg):
        # type: (dialog.settings_dialog.SettingsDialog) -> None
        # Html
        dlg.html.darkModeCheckbox.Value = self.dark_mode
        dlg.html.showSilkscreenCheckbox.Value = self.show_silkscreen
        dlg.html.highlightPin1Checkbox.Value = self.highlight_pin1
        dlg.html.continuousRedrawCheckbox.value = self.redraw_on_drag
        dlg.html.boardRotationSlider.Value = self.board_rotation
        dlg.html.bomCheckboxesCtrl.Value = self.checkboxes
        dlg.html.bomDefaultView.Selection = self.bom_view
        dlg.html.layerDefaultView.Selection = self.layer_view
        dlg.html.openBrowserCheckbox.Value = self.open_browser

        # General
        dlg.general.bomDirPicker.Path = self.bom_dest_dir
        dlg.general.componentSortOrderBox.SetItems(self.component_sort_order)
        dlg.general.blacklistBox.SetItems(self.component_blacklist)
        dlg.general.blacklistVirtualCheckbox.Value = self.blacklist_virtual

        # Extra fields
        if self.netlist_file is not None:
            dlg.extra.netlistFilePicker.Path = self.netlist_file
        else:
            dlg.extra.netlistFilePicker.SetInitialDirectory(
                    self.netlist_initial_directory)
        # TODO: load netlist/xml and set strings
        dlg.extra.extraFieldsList.SetCheckedStrings(self.extra_fields)
        dlg.extra.boardVariantFieldBox.Value = self.board_variant_field
        # TODO: load netlist/xml and set board variants
        dlg.extra.boardVariantList.SetCheckedStrings(self.board_variants)
        dlg.extra.dnpFieldBox.Value = self.dnp_field

    # noinspection PyTypeChecker
    @classmethod
    def add_options(cls, parser):
        # type: (argparse.ArgumentParser) -> None
        parser.add_argument('--show-dialog', action='store_true',
                            help='Shows config dialog. All other flags '
                                 'will be ignored.')
        # Html
        parser.add_argument('--dark-mode', help='Default to dark mode.',
                            action='store_true')
        parser.add_argument('--hide-silkscreen',
                            help='Hide silkscreen by default.',
                            action='store_true')
        parser.add_argument('--highlight-pin1',
                            help='Highlight pin1 by default.',
                            action='store_true')
        parser.add_argument('--no-redraw-on-drag',
                            help='Do not redraw pcb on drag by default.',
                            action='store_true')
        parser.add_argument('--board-rotation', type=int, default=0,
                            help='Board rotation in degrees (-180 to 180). '
                                 'Will be rounded to multiple of 5.')
        parser.add_argument('--checkboxes',
                            default=','.join(cls.default_checkboxes),
                            help='Comma separated list of checkbox columns.')
        parser.add_argument('--bom-view', default='left-right',
                            choices=cls.bom_view_choices,
                            help='Default BOM view.')
        parser.add_argument('--layer-view', default='FB',
                            choices=cls.layer_view_choices,
                            help='Default layer view.')
        parser.add_argument('--no-browser', help='Do not launch browser.',
                            action='store_true')

        # General
        parser.add_argument('--dest-dir', default='./bom/',
                            help='Destination directory for bom file '
                                 'relative to pcb file directory.')
        parser.add_argument('--sort-order',
                            help='Default sort order for components. '
                                 'Must contain "~" once.',
                            default=','.join(cls.default_sort_order))
        parser.add_argument('--blacklist', default='',
                            help='List of comma separated blacklisted '
                                 'components or prefixes with *. E.g. "X1,MH*"')
        parser.add_argument('--no-blacklist-virtual', action='store_true',
                            help='Do not blacklist virtual components.')

        # Extra fields section
        parser.add_argument('--netlist-file',
                            help='Path to netlist or xml file.')
        parser.add_argument('--extra-fields', default='',
                            help='Comma separated list of extra fields to '
                                 'pull from netlist or xml file.')
        parser.add_argument('--board-variant-field',
                            help='Name of the extra field that stores board '
                                 'variant for component.')
        parser.add_argument('--board-variants', default='',
                            help='Comma separated list of board variants to '
                                 'include in the BOM.')
        parser.add_argument('--dnp-field',
                            help='Name of the extra field that indicates '
                                 'do not populate status. Components with this '
                                 'field not empty will be blacklisted.')

    def set_from_args(self, args):
        # type: (argparse.Namespace) -> None
        import math

        # Html
        self.dark_mode = args.dark_mode
        self.show_silkscreen = not args.hide_silkscreen
        self.highlight_pin1 = args.highlight_pin1
        self.redraw_on_drag = not args.no_redraw_on_drag
        self.board_rotation = math.fmod(args.board_rotation // 5, 37)
        self.checkboxes = args.checkboxes.split(',')
        self.bom_view = self.bom_view_choices.index(args.bom_view)
        self.layer_view = self.layer_view_choices.index(args.layer_view)
        self.open_browser = not args.no_browser

        # General
        self.bom_dest_dir = args.dest_dir
        self.component_sort_order = args.sort_order.split(',')
        self.component_blacklist = args.blacklist.split(',')
        self.blacklist_virtual = not args.no_blacklist_virtual

        # Extra
        self.netlist_file = args.netlist_file
        self.extra_fields = args.extra_fields.split(',')
        self.board_variant_field = args.board_variant_field
        self.board_variants = args.board_variants.split(',')
        self.dnp_field = args.dnp_field

    def get_html_config(self):
        import json
        d = {}
        for f in self.html_config_fields:
            d[f] = getattr(self, f)
        return json.dumps(d)
