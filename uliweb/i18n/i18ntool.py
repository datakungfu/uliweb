import os
from optparse import make_option
from uliweb.core import SimpleFrame
from uliweb.utils.common import pkg
from uliweb.core.commands import Command

#def getfiles(path):
#    files_list = []
#    if os.path.exists(os.path.abspath(os.path.normcase(path))):
#        if os.path.isfile(path):
#            files_list.append(path)
#        else:
#            for root, dirs, files in os.walk(path):
#                for f in files:
#                    filename = os.path.join(root, f)
#                    if '.svn' in filename or (not filename.endswith('.py') and not filename.endswith('.html') and not filename.endswith('.ini')):
#                        continue
#                    files_list.append(filename)
#    return files_list

def _get_outputfile(path, locale='en'):
    output = os.path.normpath(os.path.join(path, 'locale', locale, 'LC_MESSAGES', 'uliweb.pot'))
    return output

def _process(path, locale, options):
    from pygettext import extrace_files
    from po_merge import merge

    output = _get_outputfile(path, locale=locale)
    try:
        extrace_files(path, output, {'verbose':options['verbose']})
        print 'Success! output file is %s' % output
        merge(output[:-4]+'.po', output)
    except:
        raise
 
class I18nCommand(Command):
    name = 'i18n'
    check_apps_dirs = False
    args = '<appname, appname, ...>'
    help = 'Extract i18n message catalog form app or all apps. Please notice that you can not set -p, -d, --uliweb, --apps and <appname, ...> at the same time.'
    has_options = True
    option_list = (
        make_option('--apps', dest='apps', action='store_true', default=False,
            help='If set, then extract translation messages from all apps located in project direcotry, and save .po file in each app direcotry.'),
        make_option('-p', dest='project', action='store_true', default=False,
            help='If set, then extract translation messages from project directory.'),
        make_option('-d', dest='directory', 
            help='If set, then extract translation messages from directory.'),
        make_option('--uliweb', dest='uliweb', action='store_true', default=False,
            help='If set, then extract translation messages from uliweb.'),
        make_option('-l', dest='locale', default='en',
            help='Target locale. Default is "en".'),
    )
    
    def handle(self, options, global_options, *args):
        opts = {'verbose':global_options.verbose}
        if options.project:
            _process(global_options.project, options.locale, opts)
        elif options.apps or args:
            if options.apps:
                _apps = SimpleFrame.get_apps(global_options.apps_dir)
            else:
                _apps = args
            apps_dir = os.path.normpath(os.path.abspath(global_options.apps_dir))
            for appname in _apps:
                path = SimpleFrame.get_app_dir(appname)
                if not path.startswith(apps_dir):
                    continue
                _process(SimpleFrame.get_app_dir(appname), options.locale, opts)
        elif options.uliweb:
            path = pkg.resource_filename('uliweb', '')
            _process(path, options.locale, opts)
        elif options.directory:
            _process(options.directory, options.locale, opts)
            
