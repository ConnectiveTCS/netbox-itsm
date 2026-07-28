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

portfolio_buttons = (
    PluginMenuButton(
        link='plugins:netbox_itsm:serviceportfolio_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN,
    ),
    PluginMenuButton(
        link='plugins:netbox_itsm:serviceportfolio_bulk_import',
        title='Import',
        icon_class='mdi mdi-upload',
        color=ButtonColorChoices.CYAN,
    ),
)

portfolio_member_buttons = (
    PluginMenuButton(
        link='plugins:netbox_itsm:serviceportfoliomember_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN,
    ),
    PluginMenuButton(
        link='plugins:netbox_itsm:serviceportfoliomember_bulk_import',
        title='Import',
        icon_class='mdi mdi-upload',
        color=ButtonColorChoices.CYAN,
    ),
)

business_capability_buttons = (
    PluginMenuButton(
        link='plugins:netbox_itsm:businesscapability_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN,
    ),
    PluginMenuButton(
        link='plugins:netbox_itsm:businesscapability_bulk_import',
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
        ('Portfolios & Capabilities', (
            PluginMenuItem(
                link='plugins:netbox_itsm:serviceportfolio_list',
                link_text='Portfolios',
                permissions=['netbox_itsm.view_serviceportfolio'],
                buttons=portfolio_buttons,
            ),
            PluginMenuItem(
                link='plugins:netbox_itsm:serviceportfoliomember_list',
                link_text='Portfolio Members',
                permissions=['netbox_itsm.view_serviceportfoliomember'],
                buttons=portfolio_member_buttons,
            ),
            PluginMenuItem(
                link='plugins:netbox_itsm:businesscapability_list',
                link_text='Business Capabilities',
                permissions=['netbox_itsm.view_businesscapability'],
                buttons=business_capability_buttons,
            ),
        )),
    ),
)
