from netbox.choices import ButtonColorChoices
from netbox.plugins import PluginMenu, PluginMenuButton, PluginMenuItem

service_buttons = (
    PluginMenuButton(
        link='plugins:netbox_itsm:service_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN,
    ),
    PluginMenuButton(
        link='plugins:netbox_itsm:service_bulk_import',
        title='Import',
        icon_class='mdi mdi-upload',
        color=ButtonColorChoices.CYAN,
    ),
)

dependency_buttons = (
    PluginMenuButton(
        link='plugins:netbox_itsm:servicedependency_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN,
    ),
    PluginMenuButton(
        link='plugins:netbox_itsm:servicedependency_bulk_import',
        title='Import',
        icon_class='mdi mdi-upload',
        color=ButtonColorChoices.CYAN,
    ),
)

asset_buttons = (
    PluginMenuButton(
        link='plugins:netbox_itsm:serviceasset_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN,
    ),
    PluginMenuButton(
        link='plugins:netbox_itsm:serviceasset_bulk_import',
        title='Import',
        icon_class='mdi mdi-upload',
        color=ButtonColorChoices.CYAN,
    ),
)

menu = PluginMenu(
    label='ITSM',
    icon_class='mdi mdi-briefcase-outline',
    groups=(
        ('Service Catalog', (
            PluginMenuItem(
                link='plugins:netbox_itsm:service_list',
                link_text='Services',
                permissions=['netbox_itsm.view_service'],
                buttons=service_buttons,
            ),
            PluginMenuItem(
                link='plugins:netbox_itsm:servicedependency_list',
                link_text='Dependencies',
                permissions=['netbox_itsm.view_servicedependency'],
                buttons=dependency_buttons,
            ),
            PluginMenuItem(
                link='plugins:netbox_itsm:serviceasset_list',
                link_text='Asset Links',
                permissions=['netbox_itsm.view_serviceasset'],
                buttons=asset_buttons,
            ),
        )),
    ),
)
