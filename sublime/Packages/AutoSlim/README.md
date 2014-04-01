AutoSlim Sublime Text 2 Plugin
================================

This plugin parses slim files, and saves the resulting HTML to the clipboard.

Installation
------------
This plugin requires ruby, with the Slim gem installed.

### Git

1. Checkout the plugin into your Packages directory

        cd PLATFOMR_PACKAGE_DIR
        git clone git://github.com/TikiTDO/AutoSlim.git

### Package Control

1. Open Command Palette - `Control+Shift+P` on Linux/Windows, `Command+Shift+P` on OS X

2. Select "Package Control: Install Package"

3. Select "AutoSlim"

Configuration
-------------

Options and Key Bindings are available in `Preferences -> Package Settings -> AutoSlim`

1. `ruby` - Path to the ruby executable
2. `run_on_save` - Automatically parse slim files to clipboard on save (Default: false)

Default hotkey for the operation is `Control+Shiftt+L` or `Command+Shift+L`
