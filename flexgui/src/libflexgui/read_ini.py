import os

from PyQt6.QtCore import QSettings

from libflexgui import dialogs

def read(parent):
	machine_name = parent.inifile.find('EMC', 'MACHINE') or False
	if machine_name:
		parent.settings = QSettings('Flex', machine_name)
	else:
		parent.settings = QSettings('Flex', 'unknown')

	units = parent.inifile.find('TRAJ', 'LINEAR_UNITS') or False # mm or inch
	if units.lower() == 'inch':
		parent.default_precision = 4
	elif units.lower() == 'mm':
		parent.default_precision = 3
	else:
		parent.default_precision = 4

	# get file extensions
	parent.extensions = ['.ngc'] # used by the touch file selector
	extensions = parent.inifile.find('DISPLAY', 'EXTENSIONS') or False
	if extensions: # add any extensions from the ini to ngc
		for ext in ini_extensions.split(','):
			parent.extensions.append(ext.strip())
		extensions = extensions.split(',')
		extensions = ' '.join(extensions).strip()
		parent.ext_filter = f'G code Files ({extensions});;All Files (*)'
	else:
		parent.ext_filter = 'G code Files (*.ngc *.NGC);;All Files (*)'

	# FIXME use rgb, rgba or hex.
	# FIXME check for FLEX-COLORS section and items and warn
	if parent.inifile.find('FLEX_COLORS', 'ESTOP_OPEN'):
		msg = ('The colors for E Stop and Power buttons\n'
		'has been moved to the [FLEXGUI] section\n'
		'of the ini file.\n'
		'See the INI Settings section of the\n'
		'documents for more information.')
		dialogs.warn_msg_ok(parent, msg, 'Update the INI file')
	parent.estop_open_color = parent.inifile.find('FLEXGUI', 'ESTOP_OPEN_COLOR') or False
	parent.estop_closed_color = parent.inifile.find('FLEXGUI', 'ESTOP_CLOSED_COLOR') or False
	parent.power_off_color =  parent.inifile.find('FLEXGUI', 'POWER_OFF_COLOR') or False
	parent.power_on_color =  parent.inifile.find('FLEXGUI', 'POWER_ON_COLOR') or False

	units = parent.inifile.find('TRAJ', 'LINEAR_UNITS') or False
	if units == 'inch':
		parent.units = 'in'
	else:
		parent.units = 'mm'

	directory = parent.inifile.find('DISPLAY', 'PROGRAM_PREFIX') or False
	if directory:
		if directory.startswith('./'): # in this directory
			parent.nc_code_dir = os.path.join(parent.ini_path, directory[2:])
		elif directory.startswith('../'): # up one directory
			parent.nc_code_dir = os.path.dirname(parent.ini_path)
		elif directory.startswith('~'): # users home directory
			parent.nc_code_dir = os.path.expanduser(directory)
		elif os.path.isdir(directory):
			parent.nc_code_dir = directory
		else:
			parent.nc_code_dir = os.path.expanduser('~/')
	elif os.path.isdir(os.path.expanduser('~/linuxcnc/nc_files')):
		parent.nc_code_dir = os.path.expanduser('~/linuxcnc/nc_files')
	else:
		parent.nc_code_dir = os.path.expanduser('~/')

	parent.editor = parent.inifile.find('DISPLAY', 'EDITOR') or False
	parent.tool_editor = parent.inifile.find('DISPLAY', 'TOOL_EDITOR') or False
	if parent.inifile.find('DISPLAY', 'LATHE') is not None:
		parent.default_view = 'y'
	elif parent.inifile.find('DISPLAY', 'VIEW') is not None:
		parent.default_view = parent.inifile.find('DISPLAY', 'VIEW')
	else:
		parent.default_view = 'p'

	parent.tool_table = parent.inifile.find('EMCIO', 'TOOL_TABLE') or False
	parent.var_file = parent.inifile.find('RS274NGC', 'PARAMETER_FILE') or False

	if parent.inifile.find('FLEX', 'PLOT_BACKGROUND_COLOR'):
		msg = ('The [FLEX] section has been changed to [FLEXGUI]\n'
		'The key PLOT_BACKGROUND_COLOR needs to be in the [FLEXGUI] section\n'
		'Check the Plotter section of the Documents for correct INI entries.')
		dialogs.warn_msg_ok(parent, msg, 'Configuration Error')

	parent.plot_background_color = parent.inifile.find('FLEXGUI', 'PLOT_BACKGROUND_COLOR') or False
	#print(type(background_color))
	#print(background_color)
	if parent.plot_background_color:
		parent.plot_background_color = tuple(map(float, parent.plot_background_color.split(',')))

	if parent.inifile.find('FLEX', 'TOUCH_FILE_WIDTH'):
		msg = ('The [FLEX] section has been changed to [FLEXGUI]\n'
		'The key TOUCH_FILE_WIDTH needs to be in the [FLEXGUI] section\n'
		'Check the Plotter section of the Documents for correct INI entries.')
		dialogs.warn_msg_ok(parent, msg, 'Configuration Error')

	parent.touch_file_width = parent.inifile.find('FLEX', 'TOUCH_FILE_WIDTH') or False
	if parent.touch_file_width in ['True', 'true', '1']:
		parent.touch_file_width = True
	else:
		parent.touch_file_width = False

	if parent.inifile.find('FLEX', 'MANUAL_TOOL_CHANGE'):
		msg = ('The [FLEX] section has been changed to [FLEXGUI]\n'
		'The key MANUAL_TOOL_CHANGE needs to be in the [FLEXGUI] section\n'
		'Check the Tools section of the Documents for correct INI entries.')
		dialogs.warn_msg_ok(parent, msg, 'Configuration Error')

	parent.manual_tool_change = parent.inifile.find('FLEXGUI', 'MANUAL_TOOL_CHANGE') or False


