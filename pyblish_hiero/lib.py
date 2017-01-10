# Standard library
import os
import sys

# Pyblish libraries
import pyblish.api

# Host libraries
import hiero
from PySide import QtGui

# Local libraries
from . import plugins

cached_process = None


self = sys.modules[__name__]
self._has_been_setup = False
self._has_menu = False
self._registered_gui = None


def setup(console=False, port=None, menu=True):
    """Setup integration

    Registers Pyblish for Hiero plug-ins and appends an item to the File-menu

    Arguments:
        console (bool): Display console with GUI
        port (int, optional): Port from which to start looking for an
            available port to connect with Pyblish QML, default
            provided by Pyblish Integration.
        menu (bool, optional): Display file menu in Hiero.
    """

    if self._has_been_setup:
        teardown()

    register_plugins()
    register_host()

    if menu:
        add_to_filemenu()
        self._has_menu = True

    self._has_been_setup = True
    print("pyblish: Loaded successfully.")


def show():
    """Try showing the most desirable GUI
    This function cycles through the currently registered
    graphical user interfaces, if any, and presents it to
    the user.
    """

    return (_discover_gui() or _show_no_gui)()


def _discover_gui():
    """Return the most desirable of the currently registered GUIs"""

    # Prefer last registered
    guis = reversed(pyblish.api.registered_guis())

    for gui in guis:
        try:
            gui = __import__(gui).show
        except (ImportError, AttributeError):
            continue
        else:
            return gui


def teardown():
    """Remove integration"""
    if not self._has_been_setup:
        return

    deregister_plugins()
    deregister_host()

    if self._has_menu:
        remove_from_filemenu()
        self._has_menu = False

    self._has_been_setup = False
    print("pyblish: Integration torn down successfully")


def remove_from_filemenu():
    raise NotImplementedError("Implement me please.")


def deregister_plugins():
    # De-register accompanying plugins
    plugin_path = os.path.dirname(plugins.__file__)
    pyblish.api.deregister_plugin_path(plugin_path)
    print("pyblish: Deregistered %s" % plugin_path)


def register_host():
    """Register supported hosts"""
    pyblish.api.register_host("hiero")


def deregister_host():
    """De-register supported hosts"""
    pyblish.api.deregister_host("nuke")


def register_plugins():
    # Register accompanying plugins
    plugin_path = os.path.dirname(plugins.__file__)
    pyblish.api.register_plugin_path(plugin_path)


def where(program):
    """DEPRECATED"""


def menu_action():
    import pyblish_hiero.lib
    pyblish_hiero.lib.show()


def add_to_filemenu():
    menu_bar = hiero.ui.menuBar()
    file_action = None
    for action in menu_bar.actions():
        if action.text().lower() == 'file':
            file_action = action

    file_menu = file_action.menu()

    action = QtGui.QAction('Publish', None)
    action.triggered.connect(menu_action)

    hiero.ui.insertMenuAction(action, file_menu, after='Close Project')
    action = file_menu.addSeparator()
    hiero.ui.insertMenuAction(action, file_menu, after='Close Project')

    # The act of initialising the action adds it to the right-click menu...
    PublishAction()


class PublishAction(QtGui.QAction):
    def __init__(self):
        QtGui.QAction.__init__(self, "Publish", None)
        self.triggered.connect(self.publish)

        for interest in ["kShowContextMenu/kTimeline",
                         "kShowContextMenukBin",
                         "kShowContextMenu/kSpreadsheet"]:
            hiero.core.events.registerInterest(interest, self.eventHandler)

        self.setShortcut("Ctrl+Alt+P")

    def publish(self):
        import pyblish_hiero.lib
        pyblish_hiero.lib.show()

    def eventHandler(self, event):

        # Add the Menu to the right-click menu
        event.menu.addAction(self)


def _show_no_gui():
    """Popup with information about how to register a new GUI
    In the event of no GUI being registered or available,
    this information dialog will appear to guide the user
    through how to get set up with one.
    """

    messagebox = QtGui.QMessageBox()
    messagebox.setIcon(messagebox.Warning)
    messagebox.setWindowIcon(QtGui.QIcon(os.path.join(
        os.path.dirname(pyblish.__file__),
        "icons",
        "logo-32x32.svg"))
    )

    spacer = QtGui.QWidget()
    spacer.setMinimumSize(400, 0)
    spacer.setSizePolicy(QtGui.QSizePolicy.Minimum,
                         QtGui.QSizePolicy.Expanding)

    layout = messagebox.layout()
    layout.addWidget(spacer, layout.rowCount(), 0, 1, layout.columnCount())

    messagebox.setWindowTitle("Uh oh")
    messagebox.setText("No registered GUI found.")

    if not pyblish.api.registered_guis():
        messagebox.setInformativeText(
            "In order to show you a GUI, one must first be registered. "
            "Press \"Show details...\" below for information on how to "
            "do that.")

        messagebox.setDetailedText(
            "Pyblish supports one or more graphical user interfaces "
            "to be registered at once, the next acting as a fallback to "
            "the previous."
            "\n"
            "\n"
            "For example, to use Pyblish Lite, first install it:"
            "\n"
            "\n"
            "$ pip install pyblish-lite"
            "\n"
            "\n"
            "Then register it, like so:"
            "\n"
            "\n"
            ">>> import pyblish.api\n"
            ">>> pyblish.api.register_gui(\"pyblish_lite\")"
            "\n"
            "\n"
            "The next time you try running this, Lite will appear."
            "\n"
            "See http://api.pyblish.com/register_gui.html for "
            "more information.")

    else:
        messagebox.setInformativeText(
            "None of the registered graphical user interfaces "
            "could be found."
            "\n"
            "\n"
            "Press \"Show details\" for more information.")

        messagebox.setDetailedText(
            "These interfaces are currently registered."
            "\n"
            "%s" % "\n".join(pyblish.api.registered_guis()))

    messagebox.setStandardButtons(messagebox.Ok)
    messagebox.exec_()
