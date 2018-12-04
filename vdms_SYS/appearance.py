# -*- coding: UTF-8 -*-

#########################################################
# Name: appearance.py
# Porpose: Used to set appearance (icons and colours)
# Writer: Gianluca Pernigoto <jeanlucperni@gmail.com>
# Copyright: (c) 2015-2018/2019 Gianluca Pernigoto <jeanlucperni@gmail.com>
# license: GPL3

# This file is part of Videomass2.

#    Videomass2 is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    Videomass2 is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Videomass2.  If not, see <http://www.gnu.org/licenses/>.

# Rev (01) November/20/2018
#########################################################

import os

class Appearance(object):
    """
    - called by bootstrap on_init -
    This class determines the paths to use to set icons on the appearance of 
    the graphical interface.
    """
    def __init__(self, installation, iconset):
        """
        The paths where the icon sets are located depend on where the program 
        is run and on which operating system.
        Each icons set is defined by the name of the folder that contains it.  
        By default the icon set is ``default``. 
        """
        if installation == 'portable':
            url = '%s/art/icons' % os.getcwd() # work current directory
            self.videomass_icon = "%s/videomass2.png" % url # 128x128
            self.wizard_icon = "%s/videomass2_wizard.png" % url # 128x128
            
        elif installation == 'standard linux':
            url = '/usr/share/videomass2/icons'
            self.videomass_icon = "/usr/share/pixmaps/videomass2.png" # 128x128
            self.wizard_icon = "/usr/share/pixmaps/videomass2_wizard.png" % url # 128x128
        # default black
        if iconset == 'Material_Design_Icons_black': # default
            self.x36 = '%s/Material_Design_Icons_black/36x36' % url
            self.x24 = '%s/Material_Design_Icons_black/24x24' % url
            self.x18 = '%s/Material_Design_Icons_black/18x18' % url
            self.icons_set()
        # default white
        elif iconset == 'Material_Design_Icons_white':
            self.x36 = '%s/Material_Design_Icons_white/36x36' % url
            self.x24 = '%s/Material_Design_Icons_black/24x24' % url
            self.x18 = '%s/Material_Design_Icons_black/18x18' % url
            self.icons_set()
        # flat-colours
        elif iconset == 'Flat_Color_Icons':
            self.x36 = '%s/Flat_Color_Icons/36x36' % url
            self.x24 = '%s/Flat_Color_Icons/24x24' % url
            self.x18 = '%s/Flat_Color_Icons/18x18' % url
            self.icons_set()
            
    def icons_set(self):
        """
        assignment path at the used icons in according to configuration file.
        """
        # main icons 32x32 - 36x36:
        icon_import = '%s/icon_import.png' % self.x36
        icon_presets = '%s/icon_presets.png' % self.x36
        icon_switchvideomass = '%s/icon_videoconversions.png' % self.x36
        icon_headphones = '%s/icon_audioconversions.png' % self.x36
        icon_process = '%s/icon_process.png' % self.x36
        icon_help = '%s/icon_help.png' % self.x36
        # x24 icons 24x24:
        icn_infosource = '%s/infosource.png' % self.x24
        icn_preview = '%s/preview.png' % self.x24
        icn_cut = '%s/cut.png' % self.x24
        icn_saveprf = '%s/saveprf.png' % self.x24
        icn_newprf = '%s/newprf.png' % self.x24
        icn_delprf = '%s/delprf.png' % self.x24
        icn_editprf = '%s/editprf.png' % self.x24
        # filters icons 24x24:
        icn_playfilters = '%s/playfilters.png' % self.x24
        icn_resetfilters = '%s/resetfilters.png' % self.x24
        # filters icons 18x18:
        ic_resize = '%s/resize.png' % self.x18
        ic_crop = '%s/crop.png' % self.x18
        ic_rotate = '%s/rotate.png' % self.x18
        ic_deinterlace = '%s/deinterlace.png' % self.x18
        ic_denoiser = '%s/denoiser.png' % self.x18
        ic_analyzes = '%s/analyzes.png' % self.x18
        ic_settings = '%s/settings.png' % self.x18
        
        return (self.videomass_icon, # 0
                icon_presets, # 1
                icon_switchvideomass, # 2
                icon_process, # 3
                icon_help, # 4
                icon_headphones, # 5
                icon_import, # 6
                icn_infosource, # 7
                icn_preview, # 8
                icn_cut, # 9
                icn_playfilters, # 10
                icn_resetfilters,  # 11
                icn_saveprf, # 12
                icn_newprf, # 13
                icn_delprf, # 14
                icn_editprf, # 15
                ic_resize, # 16
                ic_crop, # 17
                ic_rotate, # 18
                ic_deinterlace, # 19
                ic_denoiser, # 20
                ic_analyzes, # 21
                ic_settings, # 22
                self.wizard_icon, # 23
                )
            
        
