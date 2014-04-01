import os
import re
import sublime
import sublime_plugin
import subprocess


RETURN_CODES = {
    0: 'No error',
    1: 'Unclassified',
    2: 'Error in DTD',
    3: 'Validation error',
    4: 'Validation error',
    5: 'Error in schema compilation',
    6: 'Error writing output',
    7: 'Error in pattern (generated when [--pattern] option is used)',
    8: 'Error in Reader registration (generated when [--chkregister] option is used)',
    9: 'Out of memory error',
}
COMMAND_BASE = '%s --encode utf-8 %s "%s"'
ERRORS = {}
CONFIG = sublime.load_settings("xmllint.sublime-settings")


class backgroundLinter(sublime_plugin.EventListener):
    def __init__(self):
        super(backgroundLinter, self).__init__()

    def on_modified(self, view):
        if view.is_scratch():
            return

        remove_marks(view)

    # temporary disable post save actions
    # def on_post_save(self, view):
    #     if view.is_scratch():
    #         return

    #     remove_marks(view)

    #     ret = validate_xsd(view)
    #     if ret == 0 or ret == 2:
    #         return

    #     ret = validate_dtd(view)
    #     if ret == 0:
    #         return


class formatCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("save")
        format(self.view)


class validate_dtdCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        validate_dtd(self.view)


class validate_xsdCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        validate_xsd(self.view)


class show_error_listCommand(sublime_plugin.WindowCommand):
    def run(self):
        error_list_show(self.window.active_view(), self.window, error_list_on_done)


def error_list_show(view, window, on_done):
    vid = view.id()
    errors = []

    if ERRORS and vid in ERRORS:
        for error in ERRORS[vid]:
            description = error[3]
            lineno = error[2] + 1
            errors.append([description, '%s, line: %s' % (error[0], lineno)])

    window.show_quick_panel(errors, on_done)


def error_list_on_done(index):
    if index != -1:
        view = sublime.active_window().active_view()
        vid = view.id()
        if ERRORS and vid in ERRORS:
            line = ERRORS[vid][index][2] + 1
            view.run_command("goto_line", {"line": line})


def format(view):
    if not is_xml_file(view):
        return

    stdout, stderr, returncode = cmd(COMMAND_BASE % (CONFIG.get('path').encode("ascii"), '--format', view.file_name()))

    if returncode == 0:
        region = sublime.Region(0, view.size())
        document_old = view.substr(region)
        document_new = stdout.decode('utf-8').replace('\r', '')

        if document_old != document_new:
            edit = view.begin_edit()
            view.replace(edit, region, document_new)
            view.end_edit(edit)
            message(view, 'No errors', 2500)
        return 0
    else:
        parse_errors(view, stderr)

    return 2


def validate_dtd(view):
    if not is_xml_file(view):
        return

    stdout, stderr, returncode = cmd(COMMAND_BASE % (CONFIG.get('path').encode("ascii"), '--noout --valid', view.file_name()))

    if returncode == 0:
        message(view, 'No errors', 2500)
        return 0

    message(view, RETURN_CODES[returncode], 2500)
    parse_errors(view, stderr)

    return 1


def validate_xsd(view):
    if not is_xml_file(view):
        return

    schema = find_schema(view)

    stdout, stderr, returncode = cmd(COMMAND_BASE % (CONFIG.get('path').encode("ascii"), '--noout --schema "%s"' % schema, view.file_name()))

    if returncode == 0:
        message(view, 'No errors', 2500)
        return 0

    message(view, RETURN_CODES[returncode], 2500)
    parse_errors(view, stderr)

    return 1


def cmd(command):
    nenv = os.environ
    nenv['XMLLINT_INDENT'] = CONFIG.get('ident').encode("ascii")
    proc = subprocess.Popen(command, bufsize=-1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True, env=nenv)
    data = proc.communicate()
    return (data[0], data[1], proc.returncode)


def message(view, message, timeout=None):
    view.set_status('xmllint', 'XML Lint: ' + message)
    if timeout is not None:
        sublime.set_timeout(lambda: message_clear(view), timeout)


def message_clear(view):
    view.erase_status('xmllint')


def is_xml_file(view):
    return view.file_name().endswith('.xml')


def parse_errors(view, output):
    vid = view.id()
    vin = re.sub('[^\\\\/]*[\\\\/]', '', view.file_name())

    ERRORS[vid] = []
    marks = []

    errors = re.findall('(?<=[\\\\/])([^\\\\/]+):(\d+):\s*(.+)', output.replace('\r', ''))

    for error in errors:
        lineno = int(error[1]) - 1
        line = view.line(view.text_point(lineno, 0))
        ERRORS[vid].append((error[0], line, lineno, error[2]))
        if error[0] != vin:
            print 'Wrong view for %s, skipping marks' % error[0]
            continue
        marks.append(line)

    view.add_regions('xmllinterrors', marks, 'mark', 'dot', sublime.DRAW_OUTLINED)
    error_list_show(view, view.window(), error_list_on_done)


def find_schema(view):
    document = view.substr(sublime.Region(0, view.size()))
    match = re.search('xmlns:xsi=', document)
    if match:
        line = view.line(match.start())
        document_line = view.substr(line)
        location = re.search('SchemaLocation="([^"]*)', document_line)

        if location:
            if re.match('^[A-Za-z]+://', location.group(1)) is None:
                return re.sub('(?<=[\\\\/])[^\\\\/]+$', location.group(1), view.file_name())
            else:
                return location.group(1)
        else:
            view.add_regions('xmllinterrors', [line], 'mark', 'dot', sublime.DRAW_OUTLINED)

    return None


def remove_marks(view):
    ERRORS[view.id()] = []
    view.erase_regions('xmllinterrors')


def selected_line_no(view):
    selection = view.sel()
    if not selection:
        return None
    return view.rowcol(selection[0].end())[0]
