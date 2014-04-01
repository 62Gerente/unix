import sublime, sublime_plugin, os, subprocess, time

class AutoSlim(sublime_plugin.EventListener):
  def on_post_save(self, view):
    # Get the plugin settings
    self.settings = sublime.load_settings('AutoSlim.sublime-settings')
    if self.settings.get('save_to_html'):
      view.window().run_command("auto_slim", {"use_file": True})

class AutoSlimCommand(sublime_plugin.TextCommand):
  def run(self, edit, use_file = False):
    # Save the current window for future operations
    self.window = self.view.window()

    # Ensure we are operating on a slim file
    if self.view.file_name()[-5:] != '.slim':
      return False

    # Initialize the pluigin environment location
    self.plugin_path = os.path.join(sublime.packages_path(), 'AutoSlim')

    # Initialize the target file information
    self.target_path = self.view.window().active_view().file_name()
    self.target_dir = os.path.dirname(self.target_path)
    self.target_file = os.path.basename(self.target_path)

    # Initialize the plugin settings
    self.settings = sublime.load_settings('AutoSlim.sublime-settings')

    # Get the content of the current window
    self.active_view = self.view.window().active_view()
    self.buffer_region = sublime.Region(0, self.active_view.size())
    body = self.active_view.substr(self.buffer_region)

    # Execute the slim library
    slim = subprocess.Popen(self.cmd(), shell=True, cwd=self.target_dir, 
      stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Pass the code to parse
    out = slim.communicate(body)

    if (out[0] == "" and body != ""):
      # Notify of error
      sublime.error_message("Invalid Output: Check your ruby interpreter settings or console")
      print out[1].decode('utf8')
    else:
      print 'Slim Success!'
      if use_file:
        self.save_html(out[0].decode('utf8'))
      else:
        sublime.set_clipboard(out[0].decode('utf8'))

  # http://code.activestate.com/recipes/66434-change-line-endings/
  def fix_lines(self, mode, content):
    mode = mode.lower()
    if mode == 'unix':
      content = string.replace(content, '\r\n', '\n')
      content = string.replace(content, '\r', '\n')
    elif mode == 'osx':
      content = string.replace(content, '\r\n', '\r')
      content = string.replace(content, '\n', '\r')
    elif mode == 'windows':
      import re
      content = re.sub("\r(?!\n)|(?<!\r)\n", "\r\n", content)
    return content

  # Saves the generated html to an HTML file with the same prefix as the slim file
  def save_html(self, content):
    current_view = self.window.active_view()

    # Open the HTML file for writing
    base_name = self.view.file_name()[:-5]
    html_name = base_name + ".html"
    html_file = self.window.open_file(html_name)
    #while html_file.is_loading():
    print html_file.is_loading()
    time.sleep(.1)
    print html_file.is_loading()

    # Fix line endings
    content = self.fix_lines(html_file.line_endings(), content)

    # Write to the html file
    region = sublime.Region(0, html_file.size())

    edit = html_file.begin_edit()
    html_file.erase(edit, region)
    html_file.insert(edit, 0, content)
    html_file.end_edit(edit)

    html_file.run_command('save')


    # Return to previously active view
    self.window.focus_view(current_view)

  # Generate the Slim conversion command
  def cmd(self):
    # Get the ruby exec name from either the system, or from the plugin
    ruby = self.view.settings().get('ruby', self.settings.get('ruby'))
    script_path  = os.path.join(self.plugin_path, 'run_slim.rb')
    command = ruby + " '" + script_path + "'"
    return command