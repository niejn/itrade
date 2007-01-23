#!/usr/bin/env python
# ============================================================================
# Project Name : iTrade
# Module Name  : itrade_wxbook.py
#
# Description: wxPython Notebook for the Matrix
#
# The Original Code is iTrade code (http://itrade.sourceforge.net).
#
# The Initial Developer of the Original Code is	Gilles Dumortier.
#
# Portions created by the Initial Developer are Copyright (C) 2004-2007 the
# Initial Developer. All Rights Reserved.
#
# Contributor(s):
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; see http://www.gnu.org/licenses/gpl.html
#
# History       Rev   Description
# 2006-01-2x    dgil  Wrote it from itrade_wxmain.py module
# 2007-01-2x    dgil  Notebook re-architecture -> itrade_wxbook.py
# ============================================================================

# ============================================================================
# Imports
# ============================================================================

# python system
import logging

# wxPython system
import itrade_wxversion
import wx
import wx.lib.mixins.listctrl as wxl

# iTrade system
import itrade_config
from itrade_logging import *
from itrade_local import message,gMessage
from itrade_portfolio import loadPortfolio
from itrade_matrix import *
from itrade_quotes import *
from itrade_ext import *
from itrade_login import *
from itrade_currency import currencies

# iTrade wx system
from itrade_wxquote import addInMatrix_iTradeQuote,removeFromMatrix_iTradeQuote
from itrade_wxportfolio import select_iTradePortfolio,properties_iTradePortfolio
from itrade_wxoperations import open_iTradeOperations
from itrade_wxmoney import open_iTradeMoney
from itrade_wxalerts import open_iTradeAlerts
from itrade_wxcurrency import open_iTradeCurrencies
from itrade_wxabout import iTradeAboutBox
from itrade_wxhtml import iTradeHtmlWindow,iTradeLaunchBrowser
from itrade_wxlistquote import list_iTradeQuote
from itrade_wxlogin import login_UI

from itrade_wxmixin import iTrade_wxFrame

from itrade_wxpanes import iTrade_MatrixPortfolioPanel,iTrade_MatrixQuotesPanel,iTrade_MatrixStopsPanel,iTrade_MatrixIndicatorsPanel
from itrade_wxmoney import iTradeEvaluationPanel

# ============================================================================
# menu identifier
# ============================================================================

ID_OPEN = 100
ID_NEW = 101
ID_DELETE = 102
ID_SAVE = 103
ID_SAVEAS = 104
ID_EDIT = 105

ID_MANAGELIST = 110

ID_EXIT = 150

ID_PORTFOLIO = 200
ID_QUOTES = 201
ID_STOPS = 202
ID_INDICATORS = 203

ID_OPERATIONS = 210
ID_EVALUATION = 211
ID_CURRENCIES = 212
ID_ALERTS = 213

ID_COMPUTE = 221

ID_SMALL_VIEW = 230
ID_NORMAL_VIEW = 231
ID_BIG_VIEW = 232

ID_REFRESH = 240
ID_AUTOREFRESH = 241

ID_ADD_QUOTE = 300
ID_REMOVE_QUOTE = 301
ID_GRAPH_QUOTE = 310
ID_LIVE_QUOTE = 311
#ID_INTRADAY_QUOTE = 312
#ID_NEWS_QUOTE = 313
#ID_TABLE_QUOTE = 314
#ID_ANALYSIS_QUOTE = 315
#ID_BUY_QUOTE = 320
#ID_SELL_QUOTE = 321
ID_PROPERTY_QUOTE = 330

ID_ACCESS = 350
# ... free up 399

ID_LANG = 399
ID_LANG_FIRST = 400
ID_LANG_SYSTEM = 400
ID_LANG_ENGLISH = 401
ID_LANG_FRENCH = 402
ID_LANG_PORTUGUESE = 403
ID_LANG_DEUTCH = 404
ID_LANG_LAST = 404

ID_CACHE = 499
ID_CACHE_ERASE_DATA = 500
ID_CACHE_ERASE_NEWS = 501
ID_CACHE_ERASE_ALL = 510

ID_CONTENT = 800
ID_SUPPORT = 801
ID_BUG = 802
ID_DONORS = 803
ID_ABOUT = 810

# ============================================================================
# Notebook Page identifier
# ============================================================================

ID_PAGE_PORTFOLIO = 0
ID_PAGE_QUOTES = 1
ID_PAGE_STOPS = 2
ID_PAGE_INDICATORS = 3
ID_PAGE_EVALUATION = 4

# ============================================================================
# iTradeMainToolbar
#
# ============================================================================

cCONNECTED = wx.Colour(51,255,51)
cDISCONNECTED = wx.Colour(255,51,51)

class iTradeMainToolbar(wx.ToolBar):

    def __init__(self,parent,id):
        wx.ToolBar.__init__(self,parent,id,style = wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)
        self.m_parent = parent
        self._init_toolbar()

    def _init_toolbar(self):
        self._NTB2_EXIT = wx.NewId()
        self._NTB2_NEW = wx.NewId()
        self._NTB2_OPEN = wx.NewId()
        self._NTB2_EDIT = wx.NewId()
        self._NTB2_SAVE = wx.NewId()
        self._NTB2_SAVE_AS = wx.NewId()
        self._NTB2_MONEY = wx.NewId()
        self._NTB2_OPERATIONS = wx.NewId()
        self._NTB2_ALERTS = wx.NewId()
        self._NTB2_QUOTE = wx.NewId()
        self._NTB2_REFRESH = wx.NewId()
        self._NTB2_ABOUT = wx.NewId()

        self.SetToolBitmapSize(wx.Size(24,24))
        self.AddSimpleTool(self._NTB2_EXIT, wx.ArtProvider.GetBitmap(wx.ART_CROSS_MARK, wx.ART_TOOLBAR),
                           message('main_exit'), message('main_desc_exit'))
        self.AddControl(wx.StaticLine(self, -1, size=(-1,23), style=wx.LI_VERTICAL))
        self.AddSimpleTool(self._NTB2_NEW, wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR),
                           message('main_new'), message('main_desc_new'))
        self.AddSimpleTool(self._NTB2_OPEN, wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR),
                           message('main_open'), message('main_desc_open'))
        self.AddSimpleTool(self._NTB2_EDIT, wx.ArtProvider.GetBitmap(wx.ART_EXECUTABLE_FILE, wx.ART_TOOLBAR),
                           message('main_edit'), message('main_desc_edit'))
        self.AddSimpleTool(self._NTB2_SAVE, wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR),
                           message('main_save'), message('main_desc_save'))
        self.AddControl(wx.StaticLine(self, -1, size=(-1,23), style=wx.LI_VERTICAL))
        self.AddSimpleTool(self._NTB2_OPERATIONS, wx.ArtProvider.GetBitmap(wx.ART_REPORT_VIEW, wx.ART_TOOLBAR),
                           message('main_view_operations'), message('main_view_desc_operations'))
        self.AddSimpleTool(self._NTB2_MONEY, wx.Bitmap('res/money.png'),
                           message('main_view_money'), message('main_view_desc_money'))
        self.AddSimpleTool(self._NTB2_ALERTS, wx.Bitmap('res/bell.png'),
                           message('main_view_alerts'), message('main_view_desc_alerts'))
        self.AddControl(wx.StaticLine(self, -1, size=(-1,23), style=wx.LI_VERTICAL))
        self.AddSimpleTool(self._NTB2_QUOTE, wx.Bitmap('res/graph.png'),
                           message('main_quote_graph'), message('main_quote_desc_graph'))
        self.AddControl(wx.StaticLine(self, -1, size=(-1,23), style=wx.LI_VERTICAL))
        self.AddSimpleTool(self._NTB2_REFRESH, wx.Bitmap('res/refresh.png'),
                           message('main_view_refresh'), message('main_view_desc_refresh'))
        self.AddSimpleTool(self._NTB2_ABOUT, wx.Bitmap('res/about.png'),
                           message('main_about'), message('main_desc_about'))
        self.AddControl(wx.StaticLine(self, -1, size=(-1,23), style=wx.LI_VERTICAL))
        self.m_indicator = wx.StaticText(self, -1, "", size=(180,15), style=wx.ALIGN_RIGHT|wx.ST_NO_AUTORESIZE)
        self.AddControl(self.m_indicator)
        self.ClearIndicator()

        wx.EVT_TOOL(self, self._NTB2_EXIT, self.onExit)
        wx.EVT_TOOL(self, self._NTB2_NEW, self.onNew)
        wx.EVT_TOOL(self, self._NTB2_OPEN, self.onOpen)
        wx.EVT_TOOL(self, self._NTB2_EDIT, self.onEdit)
        wx.EVT_TOOL(self, self._NTB2_SAVE, self.onSave)
        wx.EVT_TOOL(self, self._NTB2_OPERATIONS, self.onOperations)
        wx.EVT_TOOL(self, self._NTB2_MONEY, self.onMoney)
        wx.EVT_TOOL(self, self._NTB2_ALERTS, self.onAlerts)
        wx.EVT_TOOL(self, self._NTB2_QUOTE, self.onQuote)
        wx.EVT_TOOL(self, self._NTB2_ABOUT, self.onAbout)
        wx.EVT_TOOL(self, self._NTB2_REFRESH, self.onRefresh)
        self.Realize()

    def onRefresh(self, event):
        self.m_parent.OnRefresh(event)

    def onOpen(self,event):
        self.m_parent.OnOpen(event)

    def onNew(self,event):
        self.m_parent.OnNew(event)

    def onEdit(self,event):
        self.m_parent.OnEdit(event)

    def onSave(self,event):
        self.m_parent.OnSave(event)

    def onExit(self,event):
        self.m_parent.OnExit(event)

    def onOperations(self,event):
        self.m_parent.OnOperations(event)

    def onMoney(self,event):
        self.m_parent.OnMoney(event)

    def onCompute(self,event):
        self.m_parent.OnCompute(event)

    def onAlerts(self,event):
        self.m_parent.OnAlerts(event)

    def onQuote(self,event):
        self.m_parent.OnGraphQuote(event)

    def onAbout(self,event):
        self.m_parent.OnAbout(event)

    # ---[ Market Indicator management ] ---

    def ClearIndicator(self):
        if itrade_config.bAutoRefreshMatrixView:
            label = message('indicator_autorefresh')
        else:
            label = message('indicator_noautorefresh')
        self.m_indicator.SetBackgroundColour(wx.NullColour)
        self.m_indicator.ClearBackground()
        self.m_indicator.SetLabel(label)

    def SetIndicator(self,market,clock):
        if clock=="::":
            label = market + ": " + message('indicator_disconnected')
            self.m_indicator.SetBackgroundColour(cDISCONNECTED)
        else:
            label = market + ": " + clock
            if label==self.m_indicator.GetLabel():
                self.m_indicator.SetBackgroundColour(wx.NullColour)
            else:
                self.m_indicator.SetBackgroundColour(cCONNECTED)
        self.m_indicator.ClearBackground()
        self.m_indicator.SetLabel(label)

# ============================================================================
# iTradeMainNotebookWindow
# ============================================================================

class iTradeMainNotebookWindow(wx.Notebook):

    def __init__(self,parent,id,page,portfolio,matrix):
        wx.Notebook.__init__(self,parent,id,style=wx.SIMPLE_BORDER|wx.NB_TOP)
        self.m_portfolio = portfolio
        self.m_matrix = matrix
        self.m_parent = parent
        self.init(parent)

        # events
        wx.EVT_NOTEBOOK_PAGE_CHANGED(self, id, self.OnPageChanged)
        wx.EVT_NOTEBOOK_PAGE_CHANGING(self, id, self.OnPageChanging)
        wx.EVT_ERASE_BACKGROUND(self,self.OnEraseBackground)

    # --- [ window management ] -------------------------------------

    def OnEraseBackground(self, evt):
        pass

    # --- [ page management ] -------------------------------------

    def init(self,parent):
        self.win = {}
        self.DeleteAllPages()

        self.win[ID_PAGE_PORTFOLIO] = iTrade_MatrixPortfolioPanel(self,parent,wx.NewId(),self.m_portfolio,self.m_matrix)
        self.AddPage(self.win[ID_PAGE_PORTFOLIO], message('page_portfolio'))

        self.win[ID_PAGE_QUOTES] = iTrade_MatrixQuotesPanel(self,parent,wx.NewId(),self.m_portfolio,self.m_matrix)
        self.AddPage(self.win[ID_PAGE_QUOTES], message('page_quotes'))

        self.win[ID_PAGE_STOPS] = iTrade_MatrixStopsPanel(self,parent,wx.NewId(),self.m_portfolio,self.m_matrix)
        self.AddPage(self.win[ID_PAGE_STOPS], message('page_stops'))

        self.win[ID_PAGE_INDICATORS] = iTrade_MatrixIndicatorsPanel(self,parent,wx.NewId(),self.m_portfolio,self.m_matrix)
        self.AddPage(self.win[ID_PAGE_INDICATORS], message('page_indicators'))

        self.win[ID_PAGE_EVALUATION] = iTradeEvaluationPanel(self,wx.NewId(),self.m_portfolio)
        self.AddPage(self.win[ID_PAGE_EVALUATION], message('page_evaluation'))

    def OnPageChanged(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        info('OnPageChanged,  old:%d, new:%d, sel:%d\n' % (old, new, sel))
        if old<>new:
            self.win[old].DoneCurrentPage()
            self.win[new].InitCurrentPage()
            self.m_parent.updateCheckItems(new)
        event.Skip()

    def OnPageChanging(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        info('OnPageChanging, old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()

    def OnRefresh(self, event):
        sel = self.GetSelection()
        self.win[sel].OnRefresh(event)

    def InitCurrentPage(self):
        sel = self.GetSelection()
        self.win[sel].InitCurrentPage()

    def DoneCurrentPage(self):
        sel = self.GetSelection()
        self.win[sel].DoneCurrentPage()

# ============================================================================
# iTradeMainWindow
#
# ============================================================================

import wx.lib.newevent
(PostInitEvent,EVT_POSTINIT) = wx.lib.newevent.NewEvent()

class iTradeMainWindow(wx.Frame,iTrade_wxFrame):

    def __init__(self,parent,portfolio,matrix):
        self.m_id = wx.NewId()
        wx.Frame.__init__(self,parent,self.m_id, "", size = ( 640,480), style = wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
        iTrade_wxFrame.__init__(self,parent, 'main')

        self.m_portfolio = portfolio
        self.m_matrix = matrix

        self.m_market = self.m_portfolio.market()
        self.m_connector = getDefaultLiveConnector(self.m_market,QLIST_INDICES)

        self.m_bookId = wx.NewId()
        self.m_book = iTradeMainNotebookWindow(self, self.m_bookId, page=-1, portfolio=self.m_portfolio,matrix=self.m_matrix)

        # link to other windows
        self.m_hOperation = None
        self.m_hMoney = None
        self.m_hAlerts = None
        self.m_hView = None
        self.m_hProperty = None
        self.m_hCurrency = None

        wx.EVT_CLOSE(self, self.OnCloseWindow)
        wx.EVT_WINDOW_DESTROY(self, self.OnDestroyWindow)

        # Set Lang then buildMenu
        self.SetLang(bDuringInit=True)
        self.buildMenu()

        # Toolbar
        self.m_toolbar = iTradeMainToolbar(self, wx.NewId())

        wx.EVT_SIZE(self, self.OnSize)
        wx.EVT_ERASE_BACKGROUND(self,self.OnEraseBackground)

        # refresh full view after window init finished
        EVT_POSTINIT(self, self.OnPostInit)
        wx.PostEvent(self,PostInitEvent())

        # last
        self.Show(True)

    # --- [ Menus ] ----------------------------------------------------------------

    def buildMenu(self):
        # the main menu
        self.filemenu = wx.Menu()
        self.filemenu.Append(ID_OPEN,message('main_open'),message('main_desc_open'))
        self.filemenu.Append(ID_NEW,message('main_new'),message('main_desc_new'))
        self.filemenu.Append(ID_SAVE,message('main_save'),message('main_desc_save'))
        self.filemenu.Append(ID_SAVEAS,message('main_saveas'),message('main_desc_saveas'))
        self.filemenu.Append(ID_DELETE,message('main_delete'),message('main_desc_delete'))
        self.filemenu.AppendSeparator()
        self.filemenu.Append(ID_EDIT,message('main_edit'),message('main_desc_edit'))
        self.filemenu.AppendSeparator()
        self.filemenu.Append(ID_MANAGELIST,message('main_managelist'),message('main_desc_managelist'))
        self.filemenu.AppendSeparator()
        self.filemenu.Append(ID_EXIT,message('main_exit'),message('main_desc_exit'))

        self.matrixmenu = wx.Menu()
        self.matrixmenu.AppendCheckItem(ID_PORTFOLIO, message('main_view_portfolio'),message('main_view_desc_portfolio'))
        self.matrixmenu.AppendCheckItem(ID_QUOTES, message('main_view_quotes'),message('main_view_desc_quotes'))
        self.matrixmenu.AppendCheckItem(ID_STOPS, message('main_view_stops'),message('main_view_desc_stops'))
        self.matrixmenu.AppendCheckItem(ID_INDICATORS, message('main_view_indicators'),message('main_view_desc_indicators'))
        self.matrixmenu.AppendSeparator()
        self.matrixmenu.AppendRadioItem(ID_SMALL_VIEW, message('main_view_small'),message('main_view_desc_small'))
        self.matrixmenu.AppendRadioItem(ID_NORMAL_VIEW, message('main_view_normal'),message('main_view_desc_normal'))
        self.matrixmenu.AppendRadioItem(ID_BIG_VIEW, message('main_view_big'),message('main_view_desc_big'))
        self.matrixmenu.AppendSeparator()
        self.matrixmenu.Append(ID_REFRESH, message('main_view_refresh'),message('main_view_desc_refresh'))
        self.matrixmenu.AppendCheckItem(ID_AUTOREFRESH, message('main_view_autorefresh'),message('main_view_desc_autorefresh'))

        self.quotemenu = wx.Menu()
        self.quotemenu.Append(ID_ADD_QUOTE, message('main_quote_add'),message('main_quote_desc_add'))
        self.quotemenu.Append(ID_REMOVE_QUOTE, message('main_quote_remove'),message('main_quote_desc_add'))
        self.quotemenu.AppendSeparator()
        self.quotemenu.Append(ID_GRAPH_QUOTE, message('main_quote_graph'),message('main_quote_desc_graph'))
        self.quotemenu.Append(ID_LIVE_QUOTE, message('main_quote_live'),message('main_quote_desc_live'))
        self.quotemenu.AppendSeparator()
        self.quotemenu.Append(ID_PROPERTY_QUOTE, message('main_quote_property'),message('main_quote_desc_property'))

        self.viewmenu = wx.Menu()
        self.viewmenu.Append(ID_OPERATIONS, message('main_view_operations'),message('main_view_desc_operations'))
        self.viewmenu.AppendCheckItem(ID_EVALUATION, message('main_view_evaluation'),message('main_view_desc_evaluation'))
        self.viewmenu.AppendSeparator()
        self.viewmenu.Append(ID_CURRENCIES, message('main_view_currencies'),message('main_view_desc_currencies'))
        self.viewmenu.Append(ID_ALERTS, message('main_view_alerts'),message('main_view_desc_alerts'))
        self.viewmenu.AppendSeparator()
        self.viewmenu.Append(ID_COMPUTE, message('main_view_compute'),message('main_view_desc_compute'))

        self.optionsmenu = wx.Menu()
        self.accessmenu = wx.Menu()

        ncon = 0
        for aname,acon in listLoginConnector():
            self.accessmenu.Append(ID_ACCESS+ncon+1, acon.name(), acon.desc())
            ncon = ncon + 1
        self.optionsmenu.AppendMenu(ID_ACCESS,message('main_options_access'),self.accessmenu,message('main_options_desc_access'))

        self.langmenu = wx.Menu()
        self.langmenu.AppendRadioItem(ID_LANG_SYSTEM, message('main_options_lang_default'),message('main_options_lang_default'))
        self.langmenu.AppendRadioItem(ID_LANG_ENGLISH, message('main_options_lang_english'),message('main_options_lang_english'))
        self.langmenu.AppendRadioItem(ID_LANG_FRENCH, message('main_options_lang_french'),message('main_options_lang_french'))
        self.langmenu.AppendRadioItem(ID_LANG_PORTUGUESE, message('main_options_lang_portuguese'),message('main_options_lang_portuguese'))
        self.langmenu.AppendRadioItem(ID_LANG_DEUTCH, message('main_options_lang_deutch'),message('main_options_lang_deutch'))
        self.optionsmenu.AppendMenu(ID_LANG,message('main_options_lang'),self.langmenu,message('main_options_desc_lang'))
        if itrade_config.lang == 255:
            self.optionsmenu.Enable(ID_LANG,False)

        self.cachemenu = wx.Menu()
        self.cachemenu.Append(ID_CACHE_ERASE_DATA, message('main_cache_erase_data'),message('main_cache_desc_erase_data'))
        self.cachemenu.Append(ID_CACHE_ERASE_NEWS, message('main_cache_erase_news'),message('main_cache_desc_erase_news'))
        self.cachemenu.AppendSeparator()
        self.cachemenu.Append(ID_CACHE_ERASE_ALL, message('main_cache_erase_all'),message('main_cache_desc_erase_all'))
        self.optionsmenu.AppendMenu(ID_CACHE,message('main_options_cache'),self.cachemenu,message('main_options_desc_cache'))

        self.helpmenu = wx.Menu()
        self.helpmenu.Append(ID_CONTENT, message('main_help_contents'),message('main_help_desc_contents'))
        self.helpmenu.AppendSeparator()
        self.helpmenu.Append(ID_SUPPORT, message('main_help_support'),message('main_help_desc_support'))
        self.helpmenu.Append(ID_BUG, message('main_help_bugs'),message('main_help_desc_bugs'))
        self.helpmenu.Append(ID_DONORS, message('main_help_donors'),message('main_help_desc_donors'))
        self.helpmenu.AppendSeparator()
        self.helpmenu.Append(ID_ABOUT, message('main_about'), message('main_desc_about'))

        # Creating the menubar
        menuBar = wx.MenuBar()

        # Adding the "filemenu" to the MenuBar
        menuBar.Append(self.filemenu,message('main_file'))
        menuBar.Append(self.matrixmenu,message('main_matrix'))
        menuBar.Append(self.viewmenu,message('main_view'))
        menuBar.Append(self.quotemenu,message('main_quote'))
        menuBar.Append(self.optionsmenu,message('main_options'))
        menuBar.Append(self.helpmenu,message('main_help'))

        # Adding the MenuBar to the Frame content
        self.SetMenuBar(menuBar)

        wx.EVT_MENU(self, ID_OPEN, self.OnOpen)
        wx.EVT_MENU(self, ID_NEW, self.OnNew)
        wx.EVT_MENU(self, ID_DELETE, self.OnDelete)
        wx.EVT_MENU(self, ID_SAVE, self.OnSave)
        wx.EVT_MENU(self, ID_SAVEAS, self.OnSaveAs)
        wx.EVT_MENU(self, ID_EDIT, self.OnEdit)
        wx.EVT_MENU(self, ID_MANAGELIST, self.OnManageList)
        wx.EVT_MENU(self, ID_EXIT, self.OnExit)
        wx.EVT_MENU(self, ID_SUPPORT, self.OnSupport)
        wx.EVT_MENU(self, ID_BUG, self.OnBug)
        wx.EVT_MENU(self, ID_DONORS, self.OnDonors)
        wx.EVT_MENU(self, ID_PORTFOLIO, self.OnPortfolio)
        wx.EVT_MENU(self, ID_QUOTES, self.OnQuotes)
        wx.EVT_MENU(self, ID_STOPS, self.OnStops)
        wx.EVT_MENU(self, ID_INDICATORS, self.OnIndicators)
        wx.EVT_MENU(self, ID_OPERATIONS, self.OnOperations)
        wx.EVT_MENU(self, ID_EVALUATION, self.OnEvaluation)
        wx.EVT_MENU(self, ID_COMPUTE, self.OnCompute)
        wx.EVT_MENU(self, ID_ALERTS, self.OnAlerts)
        wx.EVT_MENU(self, ID_CURRENCIES, self.OnCurrencies)

        wx.EVT_MENU(self, ID_ADD_QUOTE, self.OnAddQuote)
        wx.EVT_MENU(self, ID_REMOVE_QUOTE, self.OnRemoveCurrentQuote)
        wx.EVT_MENU(self, ID_GRAPH_QUOTE, self.OnGraphQuote)
        wx.EVT_MENU(self, ID_LIVE_QUOTE, self.OnLiveQuote)
        wx.EVT_MENU(self, ID_PROPERTY_QUOTE, self.OnPropertyQuote)

        wx.EVT_MENU(self, ID_SMALL_VIEW, self.OnViewSmall)
        wx.EVT_MENU(self, ID_NORMAL_VIEW, self.OnViewNormal)
        wx.EVT_MENU(self, ID_BIG_VIEW, self.OnViewBig)

        for i in range(0,ncon):
            wx.EVT_MENU(self, ID_ACCESS+i+1, self.OnAccess)

        wx.EVT_MENU(self, ID_LANG_SYSTEM, self.OnLangDefault)
        wx.EVT_MENU(self, ID_LANG_ENGLISH, self.OnLangEnglish)
        wx.EVT_MENU(self, ID_LANG_FRENCH, self.OnLangFrench)
        wx.EVT_MENU(self, ID_LANG_PORTUGUESE, self.OnLangPortuguese)
        wx.EVT_MENU(self, ID_LANG_DEUTCH, self.OnLangDeutch)

        wx.EVT_MENU(self, ID_CACHE_ERASE_DATA, self.OnCacheEraseData)
        wx.EVT_MENU(self, ID_CACHE_ERASE_NEWS, self.OnCacheEraseNews)
        wx.EVT_MENU(self, ID_CACHE_ERASE_ALL, self.OnCacheEraseAll)

        wx.EVT_MENU(self, ID_REFRESH, self.OnRefresh)
        wx.EVT_MENU(self, ID_AUTOREFRESH, self.OnAutoRefresh)
        wx.EVT_MENU(self, ID_ABOUT, self.OnAbout)

    # --- [ window management ] -------------------------------------

    def OnEraseBackground(self, evt):
        pass

    def OnPostInit(self,event):
        self.updateTitle()
        self.updateCheckItems()
        self.InitCurrentPage()

    def OnRefresh(self,event):
        self.m_book.OnRefresh(event)

    def OnSize(self, event):
        w,h = self.GetClientSizeTuple()
        self.m_toolbar.SetDimensions(0, 0, w, 32)
        self.m_book.SetDimensions(0, 32, w, h-32)
        event.Skip(False)

    def CloseLinks(self):
        if self.m_hOperation:
            self.m_hOperation.Close()
        if self.m_hMoney:
            self.m_hMoney.Close()
        if self.m_hAlerts:
            self.m_hAlerts.Close()
        if self.m_hView:
            self.m_hView.Close()
        if self.m_hProperty:
            self.m_hProperty.Close()
        if self.m_hCurrency:
            self.m_hCurrency.Close()

    def OnExit(self,e):
        if self.manageDirty(message('main_save_matrix_data')):
            self.Close(True)

    def OnCloseWindow(self, evt):
        if self.manageDirty(message('main_save_matrix_data')):
            self.DoneCurrentPage()
            self.Destroy()

    def OnDestroyWindow(self, evt):
        if evt.GetId()==self.m_id:
            self.CloseLinks()

    def InitCurrentPage(self):
        self.m_book.InitCurrentPage()

    def DoneCurrentPage(self):
        self.m_book.DoneCurrentPage()

    # --- [ menu ] -------------------------------------

    def OnOpen(self,e):
        if self.manageDirty(message('main_save_matrix_data'),fnt='open'):
            dp = select_iTradePortfolio(self,self.m_portfolio,'select')
            if dp:
                # can be long ...
                wx.SetCursor(wx.HOURGLASS_CURSOR)
                self.DoneCurrentPage()

                dp = loadPortfolio(dp.filename())
                self.NewContext(dp)

    def NewContext(self,dp):
        # can be long ...
        wx.SetCursor(wx.HOURGLASS_CURSOR)

        # close links
        self.CloseLinks()

        # change portfolio
        self.m_portfolio = dp

        self.m_matrix = createMatrix(dp.filename(),dp)
        self.m_market = self.m_portfolio.market()
        self.m_connector = getDefaultLiveConnector(self.m_market,QLIST_INDICES)

        # should be enough !
        wx.SetCursor(wx.STANDARD_CURSOR)

        # populate current view and refresh
        self.InitCurrentPage()

    def OnNew(self,e):
        if self.manageDirty(message('main_save_matrix_data'),fnt='open'):
            dp = properties_iTradePortfolio(self,None,'create')
            if dp:
                self.NewContext(dp)
                self.setDirty()

    def OnEdit(self,e):
        dp = properties_iTradePortfolio(self,self.m_portfolio,'edit')
        if dp:
            self.NewContext(dp)
            self.setDirty()

    def OnDelete(self,e):
        dp = select_iTradePortfolio(self,self.m_portfolio,'delete')
        if dp:
            properties_iTradePortfolio(self,dp,'delete')

    def OnSaveAs(self,e):
        if self.manageDirty(message('main_save_matrix_data'),fnt='open'):
            dp = properties_iTradePortfolio(self,self.m_portfolio,'rename')
            if dp:
                self.NewContext(dp)

    def OnSave(self,e):
        self.m_matrix.save(self.m_portfolio.filename())
        itrade_config.saveConfig()
        self.saveConfig()
        self.clearDirty()

    def OnSupport(self,e):
        iTradeLaunchBrowser(itrade_config.supportURL,new=True)

    def OnBug(self,e):
        iTradeLaunchBrowser(itrade_config.bugTrackerURL,new=True)

    def OnDonors(self,e):
        iTradeLaunchBrowser(itrade_config.donorsTrackerURL,new=True)

    def OnManageList(self,e):
        list_iTradeQuote(self,self.m_portfolio.market())

    def OnAbout(self,e):
        d = iTradeAboutBox(self)
        d.ShowModal()
        d.Destroy()

    def updateCheckItems(self,page=None):
        # get current page
        if not page:
            page = self.m_book.GetSelection()

        # refresh Check state based on current View
        m = self.matrixmenu.FindItemById(ID_PORTFOLIO)
        m.Check(page == ID_PAGE_PORTFOLIO)

        m = self.matrixmenu.FindItemById(ID_QUOTES)
        m.Check(page == ID_PAGE_QUOTES)

        m = self.matrixmenu.FindItemById(ID_STOPS)
        m.Check(page == ID_PAGE_STOPS)

        m = self.matrixmenu.FindItemById(ID_INDICATORS)
        m.Check(page == ID_PAGE_INDICATORS)

        m = self.viewmenu.FindItemById(ID_EVALUATION)
        m.Check(page == ID_PAGE_EVALUATION)

        m = self.matrixmenu.FindItemById(ID_AUTOREFRESH)
        m.Check(itrade_config.bAutoRefreshMatrixView)

        m = self.matrixmenu.FindItemById(ID_SMALL_VIEW)
        m.Check(itrade_config.matrixFontSize==1)

        m = self.matrixmenu.FindItemById(ID_NORMAL_VIEW)
        m.Check(itrade_config.matrixFontSize==2)

        m = self.matrixmenu.FindItemById(ID_BIG_VIEW)
        m.Check(itrade_config.matrixFontSize==3)

        if itrade_config.lang != 255:
            m = self.langmenu.FindItemById(ID_LANG_SYSTEM)
            m.Check(itrade_config.lang==0)

            m = self.langmenu.FindItemById(ID_LANG_ENGLISH)
            m.Check(itrade_config.lang==1)

            m = self.langmenu.FindItemById(ID_LANG_FRENCH)
            m.Check(itrade_config.lang==2)

            m = self.langmenu.FindItemById(ID_LANG_PORTUGUESE)
            m.Check(itrade_config.lang==3)

            m = self.langmenu.FindItemById(ID_LANG_DEUTCH)
            m.Check(itrade_config.lang==4)

        # refresh Enable state based on current View
        m = self.quotemenu.FindItemById(ID_ADD_QUOTE)
        m.Enable(page == ID_PAGE_QUOTES)

    def updateQuoteItems(self,op1,quote):
        # get current page
        page = self.m_book.GetSelection()

        m = self.quotemenu.FindItemById(ID_GRAPH_QUOTE)
        m.Enable(op1)
        m = self.quotemenu.FindItemById(ID_LIVE_QUOTE)
        m.Enable(op1 and quote.liveconnector().hasNotebook())
        m = self.quotemenu.FindItemById(ID_PROPERTY_QUOTE)
        m.Enable(op1)

        m = self.quotemenu.FindItemById(ID_REMOVE_QUOTE)
        m.Enable((page == ID_PAGE_QUOTES) and op1 and not quote.isTraded())

    def updateTitle(self):
        # get current page
        page = self.m_book.GetSelection()

        if page == ID_PAGE_PORTFOLIO:
            title = message('main_title_portfolio')
        elif page == ID_PAGE_QUOTES:
            title = message('main_title_quotes')
        elif page == ID_PAGE_STOPS:
            title = message('main_title_stops')
        elif page == ID_PAGE_INDICATORS:
            title = message('main_title_indicators')
        elif page == ID_PAGE_EVALUATION:
            title = message('main_title_evaluation')
        else:
            title = '??? %s:%s'
        self.SetTitle(title % (self.m_portfolio.name(),self.m_portfolio.accountref()))

    def RebuildList(self):
        self.DoneCurrentPage()
        self.m_matrix.build()
        self.InitCurrentPage()

    def OnPortfolio(self,e):
        # check current page
        if self.m_book.GetSelection() != ID_PAGE_PORTFOLIO:
            self.m_book.SetSelection(ID_PAGE_PORTFOLIO)
        self.updateTitle()
        self.updateCheckItems()

    def OnQuotes(self,e):
        # check current page
        if self.m_book.GetSelection() != ID_PAGE_QUOTES:
            self.m_book.SetSelection(ID_PAGE_QUOTES)
        self.updateTitle()
        self.updateCheckItems()

    def OnStops(self,e):
        # check current page
        if self.m_book.GetSelection() != ID_PAGE_STOPS:
            self.m_book.SetSelection(ID_PAGE_STOPS)
        self.updateTitle()
        self.updateCheckItems()

    def OnIndicators(self,e):
        # check current page
        if self.m_book.GetSelection() != ID_PAGE_INDICATORS:
            self.m_book.SetSelection(ID_PAGE_INDICATORS)
        self.updateTitle()
        self.updateCheckItems()

    def OnEvaluation(self,e):
        # check current page
        if self.m_book.GetSelection() != ID_PAGE_EVALUATION:
            self.m_book.SetSelection(ID_PAGE_EVALUATION)
        self.updateTitle()
        self.updateCheckItems()

    def OnOperations(self,e):
        open_iTradeOperations(self,self.m_portfolio)

    def OnCompute(self,e):
        if self.m_currentItem>=0:
            quote,item = self.getQuoteAndItemOnTheLine(self.m_currentItem)
        else:
            quote = None
        open_iTradeMoney(self,1,self.m_portfolio,quote)

    def OnAlerts(self,e):
        open_iTradeAlerts(self,self.m_portfolio)

    def OnCurrencies(self,e):
        open_iTradeCurrencies(self)

    def OnGraphQuote(self,e):
        if self.m_currentItem>=0:
            debug("OnGraphQuote: %s" % self.m_list.GetItemText(self.m_currentItem))
            self.openCurrentQuote(page=1)

    def OnLiveQuote(self,e):
        if self.m_currentItem>=0:
            debug("OnLiveQuote: %s" % self.m_list.GetItemText(self.m_currentItem))
            self.openCurrentQuote(page=2)

    def OnPropertyQuote(self,e):
        if self.m_currentItem>=0:
            debug("OnPropertyQuote: %s" % self.m_list.GetItemText(self.m_currentItem))
            self.openCurrentQuote(page=7)

    # --- [ Text font size management ] -------------------------------------

    def OnChangeViewText(self):
        itrade_config.saveConfig()
        self.updateCheckItems()
        self.m_list.SetFont(FontFromSize(itrade_config.matrixFontSize))
        for i in range(0,IDC_LAST+1):
            self.m_list.SetColumnWidth(i, wx.LIST_AUTOSIZE)

    def OnViewSmall(self,e):
        itrade_config.matrixFontSize = 1
        self.OnChangeViewText()

    def OnViewNormal(self,e):
        itrade_config.matrixFontSize = 2
        self.OnChangeViewText()

    def OnViewBig(self,e):
        itrade_config.matrixFontSize = 3
        self.OnChangeViewText()

    # --- [ Access management ] -------------------------------------

    def OnAccess(self,e):
        # get the connector
        m = self.accessmenu.FindItemById(e.GetId())
        m = m.GetText()
        c = getLoginConnector(m)
        if c:
            # with the connector, load user info and open UI
            u,p = c.loadUserInfo()
            u,p = login_UI(self,u,p,c)

            # now, save new user info
            wx.SetCursor(wx.HOURGLASS_CURSOR)
            c.saveUserInfo(u,p)
            if itrade_config.isConnected():
                # and apply these ne login info
                c.login(u,p)
            wx.SetCursor(wx.STANDARD_CURSOR)

    # --- [ Language management ] -------------------------------------

    def SetLang(self,bDuringInit=False):

        if itrade_config.lang==1:
            lang = 'us'
        elif itrade_config.lang==2:
            lang = 'fr'
        elif itrade_config.lang==3:
            lang = 'pt'
        elif itrade_config.lang==4:
            lang = 'de'
        elif itrade_config.lang==0:
            lang = gMessage.getAutoDetectedLang('us')
        else:
            # has been forced by the command line
            lang = gMessage.getLang()

        if lang != gMessage.getLang():
            gMessage.setLang(lang)
            gMessage.load()

            if not bDuringInit:
                # restore everything with the new lang
                self.CloseLinks()
                self.buildMenu()
                self.RebuildList()

        if not bDuringInit:
            self.updateCheckItems()

    def OnChangeLang(self):
        itrade_config.saveConfig()
        self.SetLang()

    def OnLangDefault(self,e):
        itrade_config.lang = 0
        self.OnChangeLang()

    def OnLangEnglish(self,e):
        itrade_config.lang = 1
        self.OnChangeLang()

    def OnLangFrench(self,e):
        itrade_config.lang = 2
        self.OnChangeLang()

    def OnLangPortuguese(self,e):
        itrade_config.lang = 3
        self.OnChangeLang()

    def OnLangDeutch(self,e):
        itrade_config.lang = 4
        self.OnChangeLang()

    # --- [ cache management ] -------------------------------------

    def OnCacheEraseData(self,e):
        dlg = wx.MessageDialog(self, message('cache_erase_confirm_data'), message('cache_erase_confirm_title'), wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
        idRet = dlg.ShowModal()
        if idRet == wx.ID_YES:
            self.m_matrix.flushTrades()
        dlg.Destroy()

    def OnCacheEraseNews(self,e):
        dlg = wx.MessageDialog(self, message('cache_erase_confirm_news'), message('cache_erase_confirm_title'), wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
        idRet = dlg.ShowModal()
        if idRet == wx.ID_YES:
            self.m_matrix.flushNews()
        dlg.Destroy()

    def OnCacheEraseAll(self,e):
        dlg = wx.MessageDialog(self, message('cache_erase_confirm_all'), message('cache_erase_confirm_title'), wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
        idRet = dlg.ShowModal()
        if idRet == wx.ID_YES:
            self.m_matrix.flushAll()
        dlg.Destroy()

    # --- [ autorefresh management ] -------------------------------------

    def OnAutoRefresh(self,e):
        self.DoneCurrentPage()
        itrade_config.bAutoRefreshMatrixView = not itrade_config.bAutoRefreshMatrixView
        itrade_config.saveConfig()
        self.updateCheckItems()
        self.m_toolbar.ClearIndicator()
        self.InitCurrentPage()

    def refreshConnexion(self):
        self.m_toolbar.SetIndicator(self.m_market,self.m_connector.currentClock())

    # ---[ Quotes ] -----------------------------------------

    def OnAddQuote(self,e):
        quote = addInMatrix_iTradeQuote(self,self.m_matrix,self.m_portfolio)
        if quote:
            self.m_portfolio.setupCurrencies()
            self.setDirty()
            self.OnQuotes(None)

    def OnRemoveCurrentQuote(self,e):
        quote,item = self.getQuoteAndItemOnTheLine(self.m_currentItem)
        if removeFromMatrix_iTradeQuote(self,self.m_matrix,quote):
            self.m_portfolio.setupCurrencies()
            self.setDirty()
            self.OnQuotes(None)

# ============================================================================
# That's all folks !
# ============================================================================