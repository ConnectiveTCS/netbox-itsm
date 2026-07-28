from netbox.plugins import PluginConfig


class NetBoxITSMConfig(PluginConfig):
    name = 'netbox_itsm'
    verbose_name = 'ITSM Service Mapping'
    description = 'Model IT services and map them to infrastructure assets'
    version = '0.1.0'
    author = 'Kyle McPherson'
    base_url = 'itsm'
    min_version = '4.6.0'

    default_settings = {
        'top_level_menu': True,
    }


config = NetBoxITSMConfig
