# -*- coding: UTF-8 -*-
# Name: showlogs.py
# Porpose: show logs data
# Compatibility: Python3, wxPython Phoenix
# Author: Gianluca Pernigoto <jeanlucperni@gmail.com>
# Copyright: (c) 2018/2020 Gianluca Pernigoto <jeanlucperni@gmail.com>
# license: GPL3
# Rev: Oct.26.2020 *PEP8 compatible*
#########################################################

# This file is part of Videomass.

#    Videomass is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    Videomass is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Videomass.  If not, see <http://www.gnu.org/licenses/>.

#########################################################
import wx
import os


class ShowLogs(wx.MiniFrame):
    """
    View log data from files within the log directory

    """
    # COLORS html
    # light
    LAVENDER = '#e6e6faff'
    NIGHT_BLUE = '#191970ff'
    # dark
    DARK_SLATE = '#1c2027ff'
    HEAVENLY = '#87ceebff'
    # breeze-blues
    SOLARIZED = '#11303eff'
    FOREST_GREEN = '#208320ff'

    # list of logs files to include
    LOGNAMES = ('ffmpeg_volumedected.log', 'youtubedl_lib.log',
                'youtubedl_exec.log', 'ffmpeg_AVconversions.log',
                'ffmpeg_presetsmanager.log', 'ffplay.log',
                'youtube_dl-update-on-AppImage.log')

    def __init__(self, parent, dirlog, OS):
        """
        Attributes defined here:
        self.dirlog > log location directory (depends from OS)
        self.logdata > dict object {KEY=file name.log: VAL=log data, ...}
        self.selected > None if item on listctrl is not selected

        """
        self.parent = parent
        self.dirlog = dirlog
        self.logdata = {}
        self.selected = None
        get = wx.GetApp()  # get data from bootstrap

        wx.MiniFrame.__init__(self, None, style=wx.CAPTION | wx.CLOSE_BOX |
                              wx.RESIZE_BORDER | wx.SYSTEM_MENU
                              )

        # ----------------------Layout----------------------#
        self.panel = wx.Panel(self, wx.ID_ANY, style=wx.TAB_TRAVERSAL)
        sizer_base = wx.BoxSizer(wx.VERTICAL)
        self.log_select = wx.ListCtrl(self.panel,
                                      wx.ID_ANY,
                                      style=wx.LC_REPORT |
                                      wx.SUNKEN_BORDER |
                                      wx.LC_SINGLE_SEL
                                      )
        self.log_select.SetMinSize((850, 200))
        self.log_select.InsertColumn(0, _('Files'), width=500)
        sizer_base.Add(self.log_select, 0, wx.ALL | wx.EXPAND, 5)
        labtxt = wx.StaticText(self.panel, label=_('Log messages'))
        sizer_base.Add(labtxt, 0, wx.ALL, 5)
        self.textdata = wx.TextCtrl(self.panel,
                                    wx.ID_ANY, "",
                                    style=wx.TE_MULTILINE |
                                    wx.TE_READONLY |
                                    wx.TE_RICH2
                                    )
        self.textdata.SetMinSize((850, 400))

        if get.THEME == 'Breeze-Blues':
            self.textdata.SetBackgroundColour(ShowLogs.SOLARIZED)
            self.textdata.SetDefaultStyle(wx.TextAttr(ShowLogs.FOREST_GREEN))
        elif get.THEME in get.DARKicons:
            self.textdata.SetBackgroundColour(ShowLogs.DARK_SLATE)
            self.textdata.SetDefaultStyle(wx.TextAttr(ShowLogs.HEAVENLY))
        else:
            self.textdata.SetBackgroundColour(ShowLogs.LAVENDER)
            self.textdata.SetDefaultStyle(wx.TextAttr(ShowLogs.NIGHT_BLUE))

        if OS == 'Darwin':
            #self.log_select.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL,
                                            #wx.NORMAL))
            self.textdata.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL,
                                          wx.NORMAL))
        else:
            #self.log_select.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL,
                                            #wx.NORMAL))
            self.textdata.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL))

        sizer_base.Add(self.textdata, 1, wx.ALL | wx.EXPAND, 5)
        # ------ btns bottom
        grdBtn = wx.GridSizer(1, 2, 0, 0)
        grid_funcbtn = wx.BoxSizer(wx.HORIZONTAL)
        button_update = wx.Button(self.panel, wx.ID_REFRESH,
                                  _("Refresh log messages"))
        grid_funcbtn.Add(button_update, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        button_clear = wx.Button(self.panel, wx.ID_CLEAR, _("Clear log messages"))
        grid_funcbtn.Add(button_clear, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        #button_delete = wx.Button(self.panel, wx.ID_REMOVE, "")
        #grid_funcbtn.Add(button_delete, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        grdBtn.Add(grid_funcbtn)
        grdexit = wx.BoxSizer(wx.HORIZONTAL)
        button_close = wx.Button(self.panel, wx.ID_CLOSE, "")
        grdexit.Add(button_close, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        grdBtn.Add(grdexit, flag=wx.ALL | wx.ALIGN_RIGHT | wx.RIGHT, border=0)
        sizer_base.Add(grdBtn, 0, wx.ALL | wx.EXPAND, 0)
        # set caption and min size
        self.SetTitle(_('Showing log messages'))
        self.SetMinSize((850, 650))
        # ------ set sizer
        self.panel.SetSizer(sizer_base)
        sizer_base.Fit(self)
        self.Layout()

        # populate ListCtrl and set self.logdata dict
        self.on_update(self)

        # ----------------------Binding (EVT)----------------------#
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_select, self.log_select)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_deselect, self.log_select)
        self.Bind(wx.EVT_BUTTON, self.on_update, button_update)
        #self.Bind(wx.EVT_BUTTON, self.on_delete, button_delete)
        self.Bind(wx.EVT_BUTTON, self.on_clear, button_clear)
        self.Bind(wx.EVT_BUTTON, self.on_close, button_close)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def onprocess(self):
        """
        Warns that changes to log files cannot be made
        during an active process

        """
        wx.MessageBox(_('In `Log View Console` mode this feature is disabled'),
                      'Videomass', wx.ICON_WARNING)
        return

    # ----------------------Event handler (callback)----------------------#

    def on_clear(self, event):
        """
        clear data logging from selected log file

        """
        if self.parent.ProcessPanel.IsShown():
            self.onprocess()
            return

        if not self.selected:
            wx.MessageBox(_('A log file must be selected'),
                          'Videomass', wx.ICON_INFORMATION)
            return

        index = self.log_select.GetFocusedItem()
        name = self.log_select.GetItemText(index, 0)

        if wx.MessageBox(_('Are you sure you want to clear the selected '
                           'log file?'), "Videomass", wx.ICON_QUESTION |
                         wx.YES_NO, self) == wx.NO:
            return

        with open(os.path.join(self.dirlog, name), 'w') as log:
            log.write('')

        self.on_update(self)
    # --------------------------------------------------------------------#

    #def on_delete(self, event):
        #"""
        #remove the selected log files found on log dir

        #"""
        #if self.parent.ProcessPanel.IsShown():
            #self.onprocess()
            #return

        #if not self.selected:
            #wx.MessageBox(_('A log file must be selected'),
                          #'Videomass', wx.ICON_INFORMATION)
            #return

        #index = self.log_select.GetFocusedItem()
        #name = self.log_select.GetItemText(index, 0)

        #if wx.MessageBox(_('Are you sure you want to delete the selected '
                         #'log file?'), "Videomass", wx.ICON_QUESTION |
                         #wx.YES_NO, self) == wx.NO:
            #return
        #try:
            #os.remove(os.path.join(self.dirlog, name))
        #except OSError as err:
            #wx.MessageBox('%s' % err, 'Videomass', wx.ICON_ERROR)
            #return

        #self.on_update(self)
    # --------------------------------------------------------------------#

    def on_update(self, event):
        """
        update data with new incoming

        """
        self.logdata.clear()
        self.log_select.DeleteAllItems()
        index = 0
        for f in os.listdir(self.dirlog):
            if os.path.basename(f) in ShowLogs.LOGNAMES:  # append listed only
            #if os.path.splitext(f)[1] == '.log':  # append all logs
                with open(os.path.join(self.dirlog, f), 'r') as log:
                    self.logdata[f] = log.read()  # set value
                    self.log_select.InsertItem(index, f)
                index += 1

        #self.on_deselect(self)
        self.log_select.Focus(0)  # make the line the current line
        self.log_select.Select(0, on=1)  # default event selection
        self.on_select(self)
    # --------------------------------------------------------------------#

    def on_deselect(self, event):
        """
        Reset on de-selected

        """
        self.textdata.Clear()
        self.selected = None
    # ------------------------------------------------------------------#

    def on_select(self, event):
        """
        show data during items selection

        """
        self.textdata.Clear()  # delete previous append:
        index = self.log_select.GetFocusedItem()
        name = self.log_select.GetItemText(index, 0)
        self.selected = name
        self.textdata.AppendText(self.logdata.get(name))
    # ------------------------------------------------------------------#

    def on_close(self, event):
        self.Destroy()
